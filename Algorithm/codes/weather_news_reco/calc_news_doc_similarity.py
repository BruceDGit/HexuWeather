"""
更新新闻推荐数据
    更新频率为 2小时
"""
import timeit
import datetime
from models.RecommentModels_v1 import NewsDocModel, DocSimilarityAlgorithm


def run():
    news_model = NewsDocModel()
    news_similarity_model = DocSimilarityAlgorithm(news_model)
    news_similarity_model.run()


if __name__ == '__main__':
    for i in range(3):
        try:
            print(timeit.timeit('run()', number=1, setup="from __main__ import run"))
            with open('/home/ubuntu/logs/HexuWeather/recognition/python_logs/calc_news_doc_similarity_py.log', 'a') as f:
                f.write('script ran successfully at {} \n\n\n'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                print('script ran successfully at {} \n\n\n'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                break
        except Exception as e:
            print('Error: ', e)
            with open('/home/ubuntu/logs/HexuWeather/recognition/python_logs/calc_news_doc_similarity_py.log', 'a') as f:
                f.write('Error:{} {} \n\n\n'.format(e, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

