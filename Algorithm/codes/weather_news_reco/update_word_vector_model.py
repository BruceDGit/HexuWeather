"""
更新词向量模型
    更新频率为 天
# 注:由于服务器内存不能满足计算要求, 因此该脚本不在线执行, 而是离线的
"""
import timeit
from models import RecommentModels_v1


def test():
    new_doc_model = RecommentModels_v1.NewsDocModel()
    new_doc_model.process_word2vec_model()


if __name__ == '__main__':
    print(timeit.timeit('test()', number=1, setup="from __main__ import test"))

