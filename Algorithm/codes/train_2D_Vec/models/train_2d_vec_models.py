"""
计算新闻关键词的2维词向量

"""
import os
import pymysql


class News2DVecModel:
    """
    2维词向量训练模型
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

    def test_seg(self):
        import jieba
        from gensim.models import Word2Vec
        # 关键词
        sql1 = "select tag from news where month(date) = 4;"
        self.cur.execute(sql1)
        result_tags = self.cur.fetchall()
        tag_lst = []
        for tag_str in result_tags:
            if tag_str:
                tags = tag_str[0].split(',')
                if tags:
                    for tag in tags:
                        if tag:
                            tag_lst.append(tag)
                            jieba.add_word(tag)
        jieba.suggest_freq(tag_lst, True)
        # 分词
        sql = "select id, context from news;"
        self.cur.execute(sql)
        results = self.cur.fetchall()
        seg_lists = []
        for tup in results:
            text = tup[1]
            seg_list = jieba.lcut(text, cut_all=False)
            seg_lists.append(seg_list)
        # 词向量模型
        if not os.path.isfile("./word2vec.model"):
            model = Word2Vec(seg_lists, size=2, window=5, min_count=1, workers=4)
            model.save("./word2vec.model")
        else:
            model = Word2Vec.load("./word2vec.model")
        # 保存
        with open('../data/test_tags.txt', 'w', encoding='utf-8') as f:
            for tag in tag_lst:
                try:
                    f.write(tag + ',' + ','.join([str(tag_vec) for tag_vec in model.wv[tag]])+'\n')
                except Exception as e:
                    pass


def test():
    news_doc = News2DVecModel()
    news_doc.test_seg()


if __name__ == '__main__':
    test()



