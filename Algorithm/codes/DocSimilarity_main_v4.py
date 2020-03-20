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
MODEL_FILE_NAME = os.path.join('./data/model_files', "news_word2vec_"+str(datetime.date.today())+".txt")
# 词向量模型备份位置
# BACKUP_MODEL_FILE_NAME = os.path.join('./data', "news_word2vec_backup_"+str(datetime.date.today())+".txt")
BACKUP_MODEL_FILE_NAME = MODEL_FILE_NAME + '.backup_' + str(time.time())
# 余弦相似度矩阵存放位置
COSINE_MATRIX_FILE_PATH = os.path.join('./data/cosine_matrix_files', "cos_matrix_"+str(datetime.date.today())+".csv")
# 余弦相似度矩阵备份位置
BACKUP_COSINE_MATRIX_FILE_PATH = COSINE_MATRIX_FILE_PATH + '.backup_' + str(time.time())
# 相关新闻的推荐数量
TOP_N = 10


class NewsDocModel:
    """
    数据模型
    提供内容如下
        1.数据库连接
        2.数据:
            增量新闻数据 get_incremental_news() return: ((id, context), (id, context), ...)
            近3个月的新闻数据 get_3m_news() return: ((id, context, date), (id, context, date), ...)
        3.方法:
            修改新闻日期类型 add_news_date()
            文本分词 segmentation()
            更新训练语料 update_segmented_corpus()
            训练词向量 get_word2vec_model()
            注-衰减系数部分暂未更新...
    """
    def __init__(self, host='localhost', port=3306, user='root', passwd='123456',
                 database='weather_user', charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.db = None
        self.cur = None
        self.connect_db()
        self.create_cursor()
        self.add_news_date()

    def connect_db(self):
        """
        连接数据库
        """
        self.db = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            database=self.database,
            charset=self.charset)

    def create_cursor(self):
        """
        创建游标对象
        """
        self.cur = self.db.cursor()

    def add_news_date(self):
        """
        将数据库news表的日期改为date类型
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

    def get_incremental_news(self):
        """
        读取增量新闻数据
        return: ((id, context), (id, context), ...)
        """

        print('开始读取增量新闻数据...', datetime.datetime.now())

        sql = "select id, context from news where text_segmentation is null;"
        self.cur.execute(sql)
        result = self.cur.fetchall()

        if not result:
            print('没有检测到新增新闻, 无需进行数据更新, 退出程序!', datetime.datetime.now())
            sys.exit()

        print('已读取到增量新闻数据!', datetime.datetime.now())

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

    def segmentation(self):
        """
        调用 pyhanlp 分词模块, 将文本语料格式转换为以空格分词的纯文本格式, 并回写入数据库
        示例: '拍摄 时 我 让 演员 放开 来 表演 , 表现 出 生活 中 那种 带有 毛边 的 质朴 ...'
        """
        corpus = self.get_incremental_news()

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
            print('分词失败, 没有新语料产生, 退出程序!', datetime.datetime.now())
            sys.exit()

    def update_segmented_corpus(self):
        """
        将熟语料拼接到一起, 保存到本地文件中, 作为词向量模型的训练数据
        文件路径: TRAIN_FILE_NAME
        """
        seg_action = self.segmentation()
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

    def get_word2vec_model(self):
        """
        加载词向量模型
        首先更新本地模型文件, 更名备份原有文件, 训练并重新保存模型
        若没有找到模型, 则直接调用hanlp的词向量模块对语料库进行词向量训练, 将得到的词向量txt文本保存到本地
        并return词向量模型
        """
        # corpus_is_updated = self.update_segmented_corpus()
        self.update_segmented_corpus()

        print('开始训练词向量...', datetime.datetime.now())

        word2vec_trainer = JClass('com.hankcs.hanlp.mining.word2vec.Word2VecTrainer')
        trainer_builder = word2vec_trainer()

        if os.path.isfile(MODEL_FILE_NAME):
            os.rename(MODEL_FILE_NAME, BACKUP_MODEL_FILE_NAME)

        word_vector_model = trainer_builder.train(TRAIN_FILE_NAME, MODEL_FILE_NAME)

        print('已完成词向量的训练, 将词向量文件保存到本地, 并返回词向量模型!', datetime.datetime.now())

        return word_vector_model

    def calculate_attenuation_coefficient(self):
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

    def get_att_coe(self):
        """
        获取近3个月新闻的衰减系数
        注: 本方法暂时没有被采用
        """
        self.calculate_attenuation_coefficient()
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
        doc2vec_train()
            构造文档向量模型, return doc_vector_model
        calculate_cosine_matrix()
            计算余弦相似度矩阵 return cosine_matrix【pandas.DataFrame类型】
        calculate_recommendation_matrix()
            计算新闻推荐top10, 数据写入数据库
        result_show()
            验证推荐结果
    """
    def __init__(self, news_doc_obj):
        self.news_doc_obj = news_doc_obj

    def doc2vec_train(self):
        """
        构造文档向量模型
        return doc_vector_model
        """
        word_vector_model = self.news_doc_obj.get_word2vec_model()
        print('开始训练文档向量模型...', datetime.datetime.now())

        doc2vec_trainer = JClass('com.hankcs.hanlp.mining.word2vec.DocVectorModel')
        doc_vector_model = doc2vec_trainer(word_vector_model)

        print('文档向量模型训练完成!', datetime.datetime.now())

        return doc_vector_model

    def calculate_cosine_matrix(self):
        """
        计算余弦相似度矩阵
        """
        print('开始余弦相似度矩阵的计算模块...', datetime.datetime.now())
        # 预加载数据
        doc_vector_model = self.doc2vec_train()
        corpus = self.news_doc_obj.get_3m_news()  # ((id, context, date), (id, context, date), ...)

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

        print('开始计算余弦相似度矩阵...', datetime.datetime.now())
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
        if os.path.isfile(COSINE_MATRIX_FILE_PATH):
            os.rename(COSINE_MATRIX_FILE_PATH, BACKUP_COSINE_MATRIX_FILE_PATH)
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

    def calculate_recommendation_matrix(self):
        """
        用对余弦相似度进行排序, 得到top10, 为每条新闻提取最相关的10条新闻, 存入数据库
        """
        print('\n', '*' * 72)
        print('程序开始...\n', datetime.datetime.now())

        self.calculate_cosine_matrix()
        cosine_matrix = pd.read_csv(COSINE_MATRIX_FILE_PATH, index_col=0)

        print('开始计算新闻推荐数据...')

        time_5 = time.time()
        # 从推荐系数矩阵中选取前10条数据, 得到新闻推荐矩阵
        top_n = TOP_N
        # recommendation_matrix = pd.DataFrame()
        # index = list(range(1, top_n+1))

        try:
            # 清空原有数据
            del_sql = 'delete from news_recommendation;'
            self.news_doc_obj.cur.execute(del_sql)

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
                self.news_doc_obj.cur.execute(sql, reco_lst)
            self.news_doc_obj.db.commit()
            time_6 = time.time()
            print('新闻推荐数据计算完成!', datetime.datetime.now())
            print("计算及保存新闻推荐数据用时:", time_6 - time_5)
            return True

        except Exception as e:
            self.news_doc_obj.db.rollback()
            print("新闻推荐数据写入数据库失败: ", e)
            return False

    """写一个SQL语句, 用关键字及新闻标题验证推荐结果是否合理"""
    def result_show(self):
        sql = ""
        self.news_doc_obj.cur.execute(sql)
        result = self.news_doc_obj.cur.fetchall()
        for item in result:
            print(item)


def test():
    news_doc = NewsDocModel()
    dsa = DocSimilarityAlgorithm(news_doc)
    dsa.calculate_recommendation_matrix()


if __name__ == '__main__':
    import timeit
    for i in range(3):
        try:
            print(timeit.timeit("test()", number=1, setup="from __main__ import test"))
            with open('/home/ubuntu/logs/HexuWeather/recognition/python_logs/DocSimilarity_python.log', 'a') as f:
                f.write('script ran successfully at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                print('script ran successfully at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '\n')
                break
        except Exception as e:
            with open('/home/ubuntu/logs/HexuWeather/recognition/python_logs/DocSimilarity_python.log', 'a') as f:
                f.write('error:{} {} \n'.format(e, datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '\n')


















