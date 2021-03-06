"""
计算新闻之间的相似度矩阵

步骤：
    1.连接数据库，读取全部新闻数据, 存入字典中
    2.调用hanlp分词模块, 将文本语料格式转换为以空格分词的纯文本格式, 如: "拍摄 时 我 让 演员 放开 来 表演 , 表现 出 生活 中 那种 带有 毛边 的 质朴 ..."
    3.调用hanlp词向量模块对语料库进行词向量训练, 得到的词向量txt文本保存到固定路径下
    4.从数据库读取近3个月的新闻数据, 存入字典中
    5.调用hanlp构造文档向量模型, 用文档向量模型计算新闻之间的余弦相似度矩阵, 存入 pandas 的 DataFrame 中, 保存到本地 csv 文件中
    6.从数据库读取近3个月新闻的日期, 计算出每条新闻的衰减系数
        注: 本次没有使用衰减系数. 经过实际效果对比, 乘上衰减系数之后, 新闻与自身的推荐系数就可能不是最大的, 无法做到剔除自身,
            且用户关心的更多是内容相关, 乘上衰减系数之后, 从新闻标题的直观印象上看推荐的相关性不强.
    7.对余弦相似度矩阵压缩得到只保留推荐系数最高的10条的新闻推荐矩阵, 将数据存储到 MySQL 数据库中
    8.写一个SQL语句, 用关键字及新闻标题验证推荐结果是否合理
"""
import datetime
import re
import time
import pandas as pd
import numpy as np

import pymysql

from pyhanlp import *

# 训练数据(熟预料)存放位置
TRAIN_FILE_NAME = os.path.join('./data', 'segmented_news_corpus.txt')
# 词向量模型存放位置
MODEL_FILE_NAME = os.path.join('./data/model_files', "news_word2vec_" + str(datetime.date.today()) + ".txt")
# 词向量模型备份位置
# BACKUP_MODEL_FILE_NAME = os.path.join('./data', "news_word2vec_backup_"+str(datetime.date.today())+".txt")
BACKUP_MODEL_FILE_NAME = MODEL_FILE_NAME + '.backup_' + str(time.time())
# 余弦相似度矩阵存放位置
COSINE_MATRIX_FILE_PATH = os.path.join('./data/cosine_matrix_files', "cos_matrix_" + str(datetime.date.today()) + ".csv")
# 余弦相似度矩阵备份位置
BACKUP_COSINE_MATRIX_FILE_PATH = COSINE_MATRIX_FILE_PATH + '.backup_' + str(time.time())
# 相关新闻的推荐数量
TOP_N = 10


class NewsDocModel:
    """
    数据模型
    对外提供内容如下
        1.数据库连接
        2.数据:
            近3个月的新闻数据 get_3m_news()
                return: ((id, context, date), (id, context, date), ...)
        3.方法:
            修改新闻日期类型(私有方法, 初始化时直接调用) __add_news_date()
            更新词向量模型 process_word2vec_model()
            加载词向量模型(静态方法) load_word2vec_model()
            注-衰减系数部分暂未更新...
    """
    def __init__(self, host='localhost', port=3306, user='root', passwd='123456',
                 database='weather_user', charset='utf8'):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__passwd = passwd
        self.__database = database
        self.__charset = charset
        self.db = None
        self.cur = None
        self.__connect_db()
        self.__create_cursor()
        self.__add_news_date()

    def __connect_db(self):
        """
        连接数据库
        """
        self.db = pymysql.connect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            passwd=self.__passwd,
            database=self.__database,
            charset=self.__charset)

    def __create_cursor(self):
        """
        创建游标对象
        """
        self.cur = self.db.cursor()

    def __add_news_date(self):
        """
        将数据库news表的日期更新为date类型
        """
        try:
            sql = '''update news
                       set date = case
                                    when length(time) = 23 then
                                     str_to_date(time, '%Y年%m月%d日 %H:%i')
                                    when length(time) = 19 then
                                     str_to_date(time, '%Y-%m-%d %H:%i:%s')
                                    when length(time) = 17 then
                                     str_to_date(time, '%Y-%m-%d %H:%i')
                                    else
                                     null
                                  end
                     where date is null;'''
            self.cur.execute(sql)
            self.db.commit()
            return True

        except Exception as e:
            print('新闻日期更新失败: ', e, datetime.datetime.now())
            self.db.rollback()
            return False

    def __get_incremental_news(self):
        """
        读取增量新闻数据
        return: ((id, context), (id, context), ...)
        """
        print('开始读取增量新闻数据...', datetime.datetime.now())

        sql = "select id, context from news where text_segmentation is null;"
        self.cur.execute(sql)
        result = self.cur.fetchall()

        print('已完成增量新闻数据的读取任务!', datetime.datetime.now())

        return result

    def get_3m_news(self):
        """
        读取近3个月的新闻数据
        return: ((id, context, date), (id, context, date), ...)
        """
        print('开始读取近3个月的新闻数据...', datetime.datetime.now())
        # 方案一: 根据标题+内容文本计算相似度
        sql = "select id, context, date from news " \
              "where date > (now() - interval 3 month);"

        # 方案二: 根据标题文本计算相似度(实验效果不理想)
        # sql = "select id, title, date from news " \
        #       "where date > (now() - interval 3 month);"

        self.cur.execute(sql)
        print('已读取到近3个月的新闻数据!', datetime.datetime.now())

        return self.cur.fetchall()

    def __segmentation(self, corpus=None):
        """
        调用 pyhanlp 分词模块, 将文本语料格式转换为以空格分词的纯文本格式, 并回写入数据库
        示例: '拍摄 时 我 让 演员 放开 来 表演 , 表现 出 生活 中 那种 带有 毛边 的 质朴 ...'
        """
        print('开始分词, 加工得到熟语料, 并回写入数据库...', datetime.datetime.now())
        HanLP.Config.ShowTermNature = False  # 修改配置使不显示词性
        try:
            for item in corpus:
                text = re.sub(r'\s', '', item[1])  # 剔除空字符

                item_segmentation_pylist = [str(term) for term in HanLP.segment(text)]
                text_segmentation = ' '.join(item_segmentation_pylist)

                sql = "update news set text_segmentation = %s where id = %s;"
                self.cur.execute(sql, [text_segmentation, item[0]])
            self.db.commit()
            print('分词成功, 已将熟语料数据写入数据库!', datetime.datetime.now())
            return True

        except Exception as e:
            self.db.rollback()
            print('Error:', e, datetime.datetime.now())
            return False

    def __update_segmented_corpus(self):
        """
        更新词向量模型的训练数据, 训练数据为拼接后的熟语料文本
        文件路径: TRAIN_FILE_NAME
        """
        print('开始更新本地熟语料文件...', datetime.datetime.now())

        # 读数据
        sql = "select text_segmentation from news;"
        self.cur.execute(sql)

        # 拼接语料
        corpus_list = []
        for item in self.cur.fetchall():
            corpus_list.append(item[0])
        corpus_doc = ' '.join(corpus_list)

        # 保存文件
        with open(TRAIN_FILE_NAME, 'w', encoding='utf-8') as f:
            f.write(corpus_doc)
        print('本地熟语料文件已更新!', datetime.datetime.now())

        return True

    def __train_word2vec_model(self):
        """
        训练词向量模型
        调用hanlp的词向量模块对语料库进行词向量训练, 将得到的词向量txt文本保存到本地
        return True
        """
        print('开始训练词向量...', datetime.datetime.now())

        word2vec_trainer = JClass('com.hankcs.hanlp.mining.word2vec.Word2VecTrainer')
        trainer_builder = word2vec_trainer()

        if os.path.isfile(MODEL_FILE_NAME):
            os.rename(MODEL_FILE_NAME, BACKUP_MODEL_FILE_NAME)

        trainer_builder.train(TRAIN_FILE_NAME, MODEL_FILE_NAME)

        print('已完成词向量的训练, 将词向量文件保存到本地!', datetime.datetime.now())
        return True

    def process_word2vec_model(self):
        """
        处理词向量模型的训练任务
            1.获取增量新闻数据
            2.对增量新闻进行空格分隔形式的分词, 存入数据库
            3.更新训练数据(拼接后的空格分隔的熟语料)
            4.训练词向量模型, 保存词向量文件到本地
        return True
        """
        print('\n', '\n', '\n')
        print('*' * 72)
        print('启动词向量训练模块...\n', datetime.datetime.now(), '\n')
        new_corpus = self.__get_incremental_news()
        if not new_corpus:
            # 没有新闻新增
            if os.path.isfile(MODEL_FILE_NAME):
                print('没有检测到新增新闻, 无需进行数据更新, 退出程序!', datetime.datetime.now())
                sys.exit()
            else:
                print('没有检测到新增新闻, 无需更新训练数据, 直接训练词向量!', datetime.datetime.now())
        else:
            seg_res = self.__segmentation(new_corpus)
            if not seg_res:
                if os.path.isfile(MODEL_FILE_NAME):
                    print('分词失败, 没有新语料产生, 无需进行数据更新, 退出程序!', datetime.datetime.now())
                    sys.exit()
                else:
                    print('分词失败, 没有新语料产生, 无需更新训练数据, 直接训练词向量!', datetime.datetime.now())
            else:
                self.__update_segmented_corpus()

        # 若训练文件不存在
        if not os.path.isfile(TRAIN_FILE_NAME):
            self.__update_segmented_corpus()

        self.__train_word2vec_model()
        return True

    @staticmethod
    def load_word2vec_model():
        """
        加载词向量模型
        """
        print('开始加载词向量模型...', datetime.datetime.now())
        if os.path.isfile(MODEL_FILE_NAME):
            WordVectorModel = JClass('com.hankcs.hanlp.mining.word2vec.WordVectorModel')
            word_vector_model = WordVectorModel(MODEL_FILE_NAME)
            print('词向量模型加载完毕!', datetime.datetime.now())
            return word_vector_model
        else:
            print('没有检测到词向量模型, 退出程序!', datetime.datetime.now())
            # self.process_word2vec_model()
            sys.exit()

    def __calculate_attenuation_coefficient(self):
        """
        根据近3个月新闻的日期, 计算出每条新闻的衰减系数, 存量数据, 一次性写入数据库
        注: 本方法目前没有被采用
        """
        print('更新衰减系数...', datetime.datetime.now())
        data = self.get_3m_news()
        try:
            for item in data:
                res = datetime.datetime.now() - item[2]
                att_coe = 0.99 ** res.days
                sql = "insert into " \
                      "news_attenuation_coefficient(new_id, attenuation_coefficient, new_date) " \
                      "values (%s, %s, %s);"
                self.cur.execute(sql, [item[0], att_coe, item[2]])
            self.db.commit()
            print('更新衰减系数成功!', datetime.datetime.now())
            return True
        except Exception as e:
            self.db.rollback()
            print("更新衰减系数失败:", e, datetime.datetime.now())
            return False

    def __get_att_coe(self):
        """
        获取近3个月新闻的衰减系数
        注: 本方法暂时没有被采用
        """
        self.__calculate_attenuation_coefficient()
        sql = "select new_id, attenuation_coefficient " \
              "  from news_attenuation_coefficient " \
              " where new_date > (now() - interval 3 month);"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        res_dict = {}
        for item in res:
            res_dict[item[0]] = item[1]
        print('读取近3月内的新闻的衰减系数!', datetime.datetime.now())
        return res_dict


class DocSimilarityAlgorithm:
    """
    新闻推荐算法
    包含如下方法:
        run()
            执行新闻推荐top10的计算任务, 计算结果写入数据库
        result_show()
            验证推荐效果
    """
    def __init__(self, news_doc_obj):
        self.__news_doc_obj = news_doc_obj

    def __doc2vec_train(self):
        """
        构造文档向量模型
        return doc_vector_model
        """
        word_vector_model = self.__news_doc_obj.load_word2vec_model()
        print('开始训练文档向量模型...', datetime.datetime.now())

        doc2vec_trainer = JClass('com.hankcs.hanlp.mining.word2vec.DocVectorModel')
        doc_vector_model = doc2vec_trainer(word_vector_model)

        print('文档向量模型训练完成!', datetime.datetime.now())

        return doc_vector_model

    def __calculate_cosine_matrix(self, doc_vector_model):
        """
        计算余弦相似度矩阵
        return cosine_matrix
        """
        print('开始计算余弦相似度矩阵...', datetime.datetime.now())
        # 预加载数据
        corpus = self.__news_doc_obj.get_3m_news()  # ((id, context, date), (id, context, date), ...)

        # 预处理
        new_corpus = []
        for item in corpus:
            tmp_a = item[0]
            tmp_b = re.sub(r'\s', '', item[1])
            new_corpus.append((tmp_a, tmp_b))

        # 初始化
        # 相似度矩阵初始为 0 矩阵
        length = len(new_corpus)
        cosine_matrix = pd.DataFrame()
        index = [item[0] for item in new_corpus]
        pds = pd.Series(np.zeros_like(index), index=index).astype(np.float)
        for idx in index:
            cosine_matrix[idx] = pds

        # 添加语料入文档向量模型
        time_1 = time.time()
        for item in new_corpus:
            doc_vector_model.addDocument(item[0], item[1])
        time_2 = time.time()

        # 计算余弦相似度
        cnt = 0
        for item in new_corpus:
            res_lst = doc_vector_model.nearest(item[1], length)
            for res in res_lst:
                res_key = res.getKey().intValue()
                res_value = res.getValue().floatValue()
                cosine_matrix[item[0]][res_key] = res_value
                cnt += 1
                if cnt % 100000 == 0:
                    print('\t已完成第 %s 次计算' %(cnt), datetime.datetime.now())
        time_3 = time.time()

        # 保存
        cosine_matrix.to_csv(COSINE_MATRIX_FILE_PATH)

        print('余弦相似度矩阵计算完成!', datetime.datetime.now())
        print('\n\n')
        print("cosine_matrix.iloc[:10, :10]:\n", cosine_matrix.iloc[:10, :10])
        print('\n\n')
        print('cosine_matrix.iloc[-10:, -10:]\n', cosine_matrix.iloc[-10:, -10:])
        print('\n\n')
        print("添加所有文档用时:", time_2-time_1)
        print("计算余弦相似度用时:", time_3-time_2)

        return cosine_matrix

    def __calculate_recommendation_matrix(self, cosine_matrix):
        """
        用对余弦相似度进行排序, 得到top10, 为每条新闻提取最相关的10条新闻, 存入数据库
        """
        # cosine_matrix = pd.read_csv(COSINE_MATRIX_FILE_PATH, index_col=0)
        print('开始计算新闻推荐数据...')

        time_5 = time.time()
        # 从推荐系数矩阵中选取前10条数据, 得到新闻推荐矩阵
        top_n = TOP_N
        # recommendation_matrix = pd.DataFrame()
        # index = list(range(1, top_n+1))

        try:
            # 清空原有数据
            del_sql = 'delete from news_recommendation;'
            self.__news_doc_obj.cur.execute(del_sql)

            for i in cosine_matrix.columns:
                new_df = cosine_matrix.sort_values(by=i, ascending=False)
                # recommendation_matrix[i] = pd.Series(new_df.index[1:top_n+1], index=index)
                reco_lst = [i]
                for idx in new_df.index[1:top_n+1]:
                    reco_lst.append(idx)
                sql = "insert into news_recommendation(" \
                      "new_id, " \
                      "reco_rank_1, reco_rank_2, reco_rank_3, reco_rank_4, reco_rank_5," \
                      "reco_rank_6, reco_rank_7, reco_rank_8, reco_rank_9, reco_rank_10) " \
                      "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                self.__news_doc_obj.cur.execute(sql, reco_lst)
            self.__news_doc_obj.db.commit()
            time_6 = time.time()
            print('新闻推荐数据计算完成!', datetime.datetime.now())
            print("计算及保存新闻推荐数据用时:", time_6 - time_5)
            return True

        except Exception as e:
            self.__news_doc_obj.db.rollback()
            print("新闻推荐数据写入数据库失败: ", e)
            return False

    def __confirm_update(self):
        """
        验证数据是否最新
            是 - 退出程序,跳过本轮计算
            否 - 正式开始计算
        """
        if os.path.isfile(COSINE_MATRIX_FILE_PATH):
            cosine_matrix_df = pd.read_csv(COSINE_MATRIX_FILE_PATH, index_col=0)
            last_index = cosine_matrix_df.index[-1]
            del cosine_matrix_df

            get_max_index_sql = "select max(id) from news;"
            self.__news_doc_obj.cur.execute(get_max_index_sql)
            res = self.__news_doc_obj.cur.fetchall()

            if last_index == res[0][0]:
                print('数据没有新增, 跳过本轮计算！')
                sys.exit()
            else:
                os.rename(COSINE_MATRIX_FILE_PATH, BACKUP_COSINE_MATRIX_FILE_PATH)

        return True

    def run(self):
        """
        执行新闻推荐top10任务
            1.验证数据是否最新
            2.构造文档向量模型
            3.计算余弦相似度矩阵
            4.为每条新闻筛选出相关新闻的top10, 写入数据库
        """
        print('\n', '\n', '\n')
        print('*' * 72)
        print('程序开始...\n', datetime.datetime.now(), '\n')

        self.__confirm_update()

        doc_vector_model = self.__doc2vec_train()
        cosine_matrix = self.__calculate_cosine_matrix(doc_vector_model)
        self.__calculate_recommendation_matrix(cosine_matrix)

    def result_show(self):
        """
        验证推荐效果
        """
        sql = """
        select t0.title '主新闻',
               t1.title '推荐新闻1',
               t2.title '推荐新闻2',
               t3.title '推荐新闻3',
               t4.title '推荐新闻4',
               t5.title '推荐新闻5',
               t6.title '推荐新闻6',
               t7.title '推荐新闻7',
               t8.title '推荐新闻8',
               t9.title '推荐新闻9',
               t10.title '推荐新闻10'
          from (select * from news_recommendation order by id desc limit 1,10)t
            left join news t0
                   on t.new_id = t0.id
            left join news t1
                   on t.reco_rank_1 = t1.id
            left join news t2
                   on t.reco_rank_2 = t2.id
            left join news t3
                   on t.reco_rank_3 = t3.id
            left join news t4
                   on t.reco_rank_4 = t4.id
            left join news t5
                   on t.reco_rank_5 = t5.id
            left join news t6
                   on t.reco_rank_6 = t6.id
            left join news t7
                   on t.reco_rank_7 = t7.id
            left join news t8
                   on t.reco_rank_8 = t8.id
            left join news t9
                   on t.reco_rank_9 = t9.id
            left join news t10
                   on t.reco_rank_10 = t10.id \G;
        """
        self.__news_doc_obj.cur.execute(sql)
        result = self.__news_doc_obj.cur.fetchall()
        for item in result:
            print(item)


def test():
    news_doc = NewsDocModel()
    dsa = DocSimilarityAlgorithm(news_doc)
    dsa.run()


if __name__ == '__main__':
    pass
    # import timeit
    # print(timeit.timeit("test()", number=1, setup="from __main__ import test"))
    # for i in range(3):
    #     try:
    #         print(timeit.timeit("test()", number=1, setup="from __main__ import test"))
    #         with open('/home/ubuntu/logs/HexuWeather/recognition/python_logs/DocSimilarity_python.log', 'a') as f:
    #             f.write('script ran successfully at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    #             print('script ran successfully at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '\n')
    #             break
    #     except Exception as e:
    #         with open('/home/ubuntu/logs/HexuWeather/recognition/python_logs/DocSimilarity_python.log', 'a') as f:
    #             f.write('error:{} {} \n'.format(e, datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '\n')


















