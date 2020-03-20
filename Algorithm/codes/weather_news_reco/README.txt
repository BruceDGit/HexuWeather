1)base_init_of_db_struc.py脚本只在数据库初始化时执行一次, 目的是为了增加一些字段和数据表, 以后不需要再执行本脚本.
2)update_word_vector_model.py脚本作用为更新词向量模型, 但是由于服务器内存较小, 导致无法执行, 因而改为定期离线执行, 然后将词向量文件上传服务器.
3)calc_news_doc_similarity.py脚本作用为计算新闻推荐top10, 设定为每两小时执行一次.
4)models/RecommentModels_v1.py为模型文件, 可从该处调用出数据模型类和计算模型类.
5)NewsKeywords_main.py为关键词加工脚本, 暂时没有启用.