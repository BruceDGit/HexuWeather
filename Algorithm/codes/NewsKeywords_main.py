"""
对近三个月的新闻提取关键字

步骤：
    1.连接数据库，读取近三个月的新闻数据
    2.调用hanlp模块进行关键词/二元短语提取
    3.将关键词存入数据库
"""

import pymysql
import pandas as pd
from pyhanlp import *
import re


class NewsKeywordsAlgorithm:
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

    # 连接数据库
    def connect_db(self):
        self.db = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            database=self.database,
            charset=self.charset
        )

    # 创建游标对象
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 读取近三个月的新闻数据(id, title, context, tag, time)
    def get_3m_news(self):
        sql = "select id, title, context, tag, date from news where date > (now() - interval 3 month);"
        self.cur.execute(sql)
        # 返回历史记录
        return self.cur.fetchall()

    """将java的ArrayList数据转换为python字符串"""
    def java_array_2_py_string(self, java_list):
        return ','.join(re.findall(r'[^\[|\]|\W|\d]+', java_list.toString()))

    """基于tf-idf的关键词提取"""
    def tf_idf(self, new_ids, new_contents):
        """
        测试：
            2362条新闻，5个关键词/条
            用时：4.85秒
        返回格式： {1063: '宗教,学员,新疆,极端主义,极端化', 1065: '董事长,陕西,集团,年薪,果业'}
        """
        tf_idf_counter = JClass('com.hankcs.hanlp.mining.word.TfIdfCounter')
        counter = tf_idf_counter()

        for new_id, new_content in zip(new_ids, new_contents):
            counter.add(new_id, new_content)  # 输入多篇文档
        counter.compute()  # 输入完毕
        # for new_id in counter.documents():
        #     print(str(new_id) + " : " + counter.getKeywordsOf(new_id, 5).toString())  # 根据每篇文档的TF-IDF提取关键词

        dict = {}
        for new_id in counter.documents():
            keyword_list = counter.getKeywordsOf(new_id, 5)
            dict[int(new_id)] = self.java_array_2_py_string(keyword_list)

        return dict

    """基于TextRank的关键词提取"""
    def text_rank(self, new_ids, new_contents):
        """
        测试：
            2362条新闻，5个关键词/条
            用时：21.63秒
        返回格式： {1063: '学员,新疆,宗教,极端主义,中国', 1065: '董事长,陕西,集团,国企,年薪'}
        """
        dict = {}
        for new_id, new_content in zip(new_ids, new_contents):
            keyword_list = HanLP.extractKeyword(new_content, 5)
            dict[int(new_id)] = self.java_array_2_py_string(keyword_list)
            # print(str(new_id) + " : " + str(keyword_list))

        return dict

    """基于PhraseExtractor的关键词提取"""
    def phrase_extract(self, new_ids, new_contents):
        """
        测试：
            2362条新闻，5个关键词/条
            用时：7.63秒
        返回格式： {1064: '宗教极端主义,反恐极端化,极端思想,中国人民,和谐稳定', 1065: '集团董事长,年度国企,高薪酬,国企高,产业集团'}
        """
        dict = {}
        for new_id, new_content in zip(new_ids, new_contents):
            phrase_list = HanLP.extractPhrase(new_content, 5)
            dict[int(new_id)] = self.java_array_2_py_string(phrase_list)
            # print(str(new_id) + " : " + str(phrase_list))

        return dict

    """保存三种方式抽取到的关键词"""
    def save_keywords(self):
        news_data = self.get_3m_news()
        news_df = pd.DataFrame(list(news_data), columns=['id', 'title', 'context', 'tag', 'date'])

        tfidf_dict = self.tf_idf(news_df['id'], news_df['context'])
        tr_dict = self.text_rank(news_df['id'], news_df['context'])
        phrase_dict = self.phrase_extract(news_df['id'], news_df['context'])

        try:
            for new_id, new_tag, new_date in news_df[['id', 'tag', 'date']].values:
                tfidf_keywords = tfidf_dict[new_id]
                tr_keywords = tr_dict[new_id]
                phrase_keywords = phrase_dict[new_id]
                # print(new_id, tfidf_keywords, tr_keywords, phrase_keywords)
                sql = "insert into news_keywords(" \
                      "new_id, tf_idf_keywords, text_rank_keywords, phrase_keywords, native_tags, news_date)\
                       values(%s, %s, %s, %s, %s, %s)"
                self.cur.execute(sql, [new_id, tfidf_keywords, tr_keywords, phrase_keywords, new_tag, new_date.date()])
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(e)
            return False


if __name__ == '__main__':
    na = NewsKeywordsAlgorithm()
    res = na.save_keywords()
    if res:
        print("insert successfully!")





























