--add date column
alter table news add date datetime default null after time; --新增日期格式的字段
alter table news add text_segmentation longtext default null after context;  --新增熟语料字段, 存储空格分词的纯文本

--update data of date
update news
   set date = case
                when length(time) = 23 then
                -- str_to_date('2019年11月25日 18:57', '%Y年%m月%d日 %H:%i')
                 str_to_date(time, '%Y年%m月%d日 %H:%i')
                when length(time) = 19 then
                -- str_to_date('2019-01-20 16:01:45', '%Y-%m-%d %H:%i:%s')
                 str_to_date(time, '%Y-%m-%d %H:%i:%s')
                when length(time) = 17 then
                -- str_to_date('2019-01-20 16:01', '%Y-%m-%d %H:%i')
                 str_to_date(time, '%Y-%m-%d %H:%i')
                else
                 null
              end
 where date is null;

select count(*) from news where date is null;

select count(*) from news where date > (now() - interval 3 month);

--news的关键词表
create table news_keywords(
    id int(11) primary key auto_increment,
    new_id int(11) not null,
    tf_idf_keywords varchar(512) not null,
    text_rank_keywords varchar(512) not null,
    phrase_keywords varchar(1024) not null
)default charset=utf8;

alter table news_keywords add news_date datetime not null;
alter table news_keywords add native_tags varchar(512) after phrase_keywords;

--news的衰减系数表
create table news_attenuation_coefficient(
    id int(11) primary key auto_increment,
    new_id int(11) not null,
    attenuation_coefficient decimal(21, 20) default 0.99 not null,
    new_date datetime not null
)default charset=utf8;
alter table news_attenuation_coefficient add unique(new_id);


--news 的推荐表
create table news_recommendation(
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
)default charset=utf8;
alter table news_attenuation_coefficient add unique(new_id);


------------------

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



--------------------------------------------------------------------
--初始化数据
truncate table news_recommendation;
update news set text_segmentation = null;

update news set text_segmentation = null where id > 3526;





















