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

TRAIN_FILE_NAME = os.path.join('./data', 'segmented_news_corpus.txt')
MODEL_FILE_NAME = os.path.join('./data', "news_word2vec.txt")
COSINE_MATRIX_FILE_PATH = os.path.join('./data/cosine_matrix_files', "cos_matrix_"+str(datetime.date.today())+".csv")


class NewsDocModel:
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

    """连接数据库"""
    def connect_db(self):
        self.db = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            database=self.database,
            charset=self.charset
        )

    def create_cursor(self):
        self.cur = self.db.cursor()

    """读取全部新闻数据, 为训练词向量做准备, return: ((id, context), (id, context), ...)"""
    def get_all_news(self):
        sql = "select id, context from news where text_segmentation is null;"
        self.cur.execute(sql)

        print('已读取到 全部新闻数据!', datetime.datetime.now())
        return self.cur.fetchall()

    """读取近3个月的新闻数据【id context date】, 存入字典中"""
    def get_3m_news(self):
        sql = "select id, context, date from news where date > (now() - interval 3 month);"
        self.cur.execute(sql)

        print('已读取到 近3个月的新闻数据!', datetime.datetime.now())
        return self.cur.fetchall()

    """调用hanlp分词模块, 将文本语料格式转换为以空格分词的纯文本格式, 并回写入数据库, 如: '拍摄 时 我 让 演员 放开 来 表演 , 表现 出 生活 中 那种 带有 毛边 的 质朴 ...'"""
    def segmentation(self):
        print('开始分词, 获取熟语料, 并回写入数据库各记录中...', datetime.datetime.now())
        corpus = self.get_all_news()
        HanLP.Config.ShowTermNature = False  # 修改配置使不显示词性
        try:
            for item in corpus:
                # crf_segment_model = HanLP.newSegment("crf")
                # item_segmentation = crf_segment_model.seg(item[1])
                text = re.sub(r'\s', '', item[1])
                item_segmentation_pylist = [str(term) for term in HanLP.segment(text)]
                text_segmentation = ' '.join(item_segmentation_pylist)

                sql = "update news set text_segmentation = %s where id = %s;"
                self.cur.execute(sql, [text_segmentation, item[0]])
            self.db.commit()
            print('分词成功, 已将 熟预料数据 更新至 数据库!', datetime.datetime.now())
            return True
        except Exception as e:
            self.db.rollback()
            print('分词失败:', e, datetime.datetime.now())
            return False

    """将熟语料拼接到一起, 保存到本地文件中, 作为词向量模型的训练数据"""
    def get_segmented_corpus(self):
        self.segmentation()
        sql = "select text_segmentation from news;"
        self.cur.execute(sql)
        corpus_list = []
        for item in self.cur.fetchall():
            corpus_list.append(item[0])
        corpus_doc = ' '.join(corpus_list)
        with open(TRAIN_FILE_NAME, 'w', encoding='utf-8') as f:
            f.write(corpus_doc)
        print('本地熟语料文件 已更新!', datetime.datetime.now())
        return True

    """调用hanlp词向量模块对语料库进行词向量训练, 得到的词向量txt文本保存到固定路径下"""
    def word2vec_train(self):
        print('开始训练词向量...', datetime.datetime.now())
        self.get_segmented_corpus()

        # if os.path.isfile(MODEL_FILE_NAME):
        #     os.remove(MODEL_FILE_NAME)
        if os.path.isfile(MODEL_FILE_NAME):
            word2vec_loader = JClass('com.hankcs.hanlp.mining.word2vec.WordVectorModel')
            word_vector_model = word2vec_loader(MODEL_FILE_NAME)
            print('检测到本地词向量模型, 直接进行加载!', datetime.datetime.now())
            return word_vector_model

        word2vec_trainer = JClass('com.hankcs.hanlp.mining.word2vec.Word2VecTrainer')
        trainer_builder = word2vec_trainer()
        word_vector_model = trainer_builder.train(TRAIN_FILE_NAME, MODEL_FILE_NAME)
        print('已完成 词向量 的训练, 将 词向量文件 保存到本地, 并返回 词向量模型!', datetime.datetime.now())
        return word_vector_model

    """根据近3个月新闻的日期, 计算出每条新闻的衰减系数, 存量数据, 一次性写入数据库"""
    def calculate_attenuation_coefficient(self):
        import datetime

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
            print('更新 衰减系数 成功!', datetime.datetime.now())
            return True
        except Exception as e:
            self.db.rollback()
            print("更新 衰减系数 失败:", e, datetime.datetime.now())
            return False

    """获取近3个月新闻的衰减系数"""
    def get_att_coe(self):
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
    def __init__(self, news_doc_obj):
        self.news_doc_obj = news_doc_obj

    """调用hanlp构造文档向量模型, 用文档向量模型计算新闻之间的余弦相似度矩阵, 存入 pandas 的 DataFrame 中"""
    def doc2vec_train(self):
        print('开始训练文档向量模型...', datetime.datetime.now())
        doc2vec_trainer = JClass('com.hankcs.hanlp.mining.word2vec.DocVectorModel')
        doc_vector_model = doc2vec_trainer(self.news_doc_obj.get_word2vec_model())
        print('文档向量模型 训练完成!', datetime.datetime.now())
        return doc_vector_model

    """计算新闻之间的余弦相似度矩阵"""
    def calculate_cosine_matrix(self):
        print('开始 余弦相似度矩阵的计算 模块...', datetime.datetime.now())
        # 预加载数据
        doc_vector_model = self.doc2vec_train()
        corpus = self.news_doc_obj.get_3m_news()  # 【id context date】

        new_corpus = []
        for item in corpus:
            tmp_a = item[0]
            tmp_b = re.sub(r'\s', '', item[1])
            new_corpus.append((tmp_a, tmp_b))
        length = len(new_corpus)

        # 初始化相似度矩阵为 0 矩阵
        cosine_matrix = pd.DataFrame()
        index = [item[0] for item in new_corpus]
        pds = pd.Series(np.zeros_like(index), index=index).astype(np.float)
        for idx in index:
            cosine_matrix[idx] = pds

        # 计算余弦相似度, 并将数据存入相似度矩阵
        print('开始 计算 余弦相似度矩阵...', datetime.datetime.now())
        time_1 = time.time()
        # 添加语料入文档向量模型
        for item in new_corpus:
            doc_vector_model.addDocument(item[0], item[1])
        time_2 = time.time()
        # 计算余弦相似度
        cnt = 0
        # for i in range(length//2+1):
        #     item = new_corpus[i]
        for item in new_corpus:
            res_lst = doc_vector_model.nearest(item[1], length)
            for res in res_lst:
                res_key = res.getKey().intValue()
                res_value = res.getValue().floatValue()
                # todo 重新执行一遍程序, 记录各程序部分消耗的时间
                #  不能只计算矩阵的一半, 以为程序是矩阵的行计算的, 不到最后右下角部分是计算不到的
                cosine_matrix[item[0]][res_key] = res_value
                cnt += 1
                if cnt % 10000 == 0:
                    print('\t已完成第 %s 次计算' %(cnt), datetime.datetime.now())
        time_3 = time.time()

        cosine_matrix.to_csv(COSINE_MATRIX_FILE_PATH)
        print()
        print("cosine_matrix.iloc[:20, :20]:\n", cosine_matrix.iloc[:20, :20])
        print('-*'*45)
        print('cosine_matrix.iloc[-20:, -20:]\n', cosine_matrix.iloc[-20:, -20:])
        print("添加所有文档用时:", time_2-time_1)
        print("计算余弦相似度用时:", time_3-time_2)

        # sys.exit()

        print('余弦相似度矩阵 计算完成!', datetime.datetime.now())
        return cosine_matrix

    """用余弦相似度和衰减系数相乘, 得到推荐系数, 并为每条新闻提取最相关的10条新闻, 存入数据库"""
    def calculate_recommendation_matrix(self):

        print('程序开始...')
        # 获取衰减系数: {id:coe, id:coe, ...}
        # att_coe = self.news_doc_obj.get_att_coe()
        # cosine_matrix = self.calculate_cosine_matrix()
        cosine_matrix = pd.read_csv(COSINE_MATRIX_FILE_PATH, index_col=0)
        print(cosine_matrix.iloc[:10, :10])

        print('开始计算 新闻推荐矩阵...')
        # 余弦相似度矩阵乘上衰减系数得到推荐系数矩阵
        # 考虑到乘上衰减系数之后, 新闻与自身的推荐系数就可能不是最大的, 无法做到剔除自身, 且用户关心的更多是内容相关, 去除衰减系数在逻辑上也合理
        # time_4 = time.time()
        # for i in att_coe.keys():
        #     cosine_matrix.loc[i] = cosine_matrix.loc[i] * float(att_coe[i])
        time_5 = time.time()

        # 从推荐系数矩阵中选取前10条数据, 得到新闻推荐矩阵
        # recommendation_matrix = pd.DataFrame()
        top_n = 10
        index = list(range(1, top_n+1))

        try:
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
            print('新闻推荐矩阵 计算完成!', datetime.datetime.now())
            print("计算 新闻推荐矩阵 用时:", time_6 - time_5)
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
    print(timeit.timeit("test()", number=1, setup="from __main__ import test"))
    # print(news_doc.get_att_coe())


















