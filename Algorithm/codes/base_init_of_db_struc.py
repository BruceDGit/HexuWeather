import datetime

from models.RecommentModels import NewsDocModel


def alter_weather_user_db():
    db_model = NewsDocModel()

    try:
        # 新增日期格式的字段,
        # 新增熟语料字段, 存储空格分词的纯文本
        news_sql1 = "alter table news add date datetime default null after time;"
        news_sql2 = "alter table news add text_segmentation longtext default null after context;"
        db_model.cur.execute(news_sql1)
        db_model.cur.execute(news_sql2)
        db_model.db.commit()
        print('成功修改 news 表结构', datetime.datetime.now())

    except Exception as e:
        db_model.db.rollback()
        print('修改 news 表结构失败: ', e)

    try:
        # 创建新闻关键词表
        news_kwd_sql1 = '''create table news_keywords(
                            id int(11) primary key auto_increment,
                            new_id int(11) not null,
                            tf_idf_keywords varchar(512) not null,
                            text_rank_keywords varchar(512) not null,
                            phrase_keywords varchar(1024) not null
                        )default charset=utf8;'''
        news_kwd_sql2 = "alter table news_keywords add news_date datetime not null;"
        news_kwd_sql3 = "alter table news_keywords add native_tags varchar(512) after phrase_keywords;"
        db_model.cur.execute(news_kwd_sql1)
        db_model.cur.execute(news_kwd_sql2)
        db_model.cur.execute(news_kwd_sql3)
        db_model.db.commit()
        print('成功创建新闻关键词表', datetime.datetime.now())

    except Exception as e:
        db_model.db.rollback()
        print('创建新闻关键词表失败: ', e)

    try:
        # 创建新闻推荐表
        news_reco_sql1 = '''create table news_recommendation(
                            id int(11) primary key auto_increment,
                            new_id int(11) not null,  # 新闻id
                            reco_rank_1 int(11) not null,  # 推荐新闻1
                            reco_rank_2 int(11) not null,
                            reco_rank_3 int(11) not null,
                            reco_rank_4 int(11) not null,
                            reco_rank_5 int(11) not null,
                            reco_rank_6 int(11) not null,
                            reco_rank_7 int(11) not null,
                            reco_rank_8 int(11) not null,
                            reco_rank_9 int(11) not null,
                            reco_rank_10 int(11) not null
                        )default charset=utf8;'''
        news_reco_sql2 = "alter table news_recommendation add unique(new_id);"
        db_model.cur.execute(news_reco_sql1)
        db_model.cur.execute(news_reco_sql2)
        db_model.db.commit()
        print('成功创建新闻推荐表', datetime.datetime.now())

    except Exception as e:
        db_model.db.rollback()
        print('创建新闻推荐表失败: ', e)


if __name__ == '__main__':
    alter_weather_user_db()