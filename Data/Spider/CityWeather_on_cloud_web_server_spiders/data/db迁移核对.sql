select count(*) from news;
-- 1093
select count(*) from request_finger;
--1278
select count(*) from sevendaysweather;
--300
select count(*) from tjnews;
--111
select count(*) from trafficnews ;
--82
select count(*) from travelnews;
--37
select count(*) from weathernews ;
--79



-- 从吴迪的数据库(weatherdb)更近近一个月的数据到项目数据库(weather_user)

select count(*) from weatherdb.news a where a.title not in (select title from weather_user.news);
-- 144
insert into weather_user.news (newsurl,title,categoryid,time,source,tag,context,author,imgurl,part)
select newsurl,title,categoryid,time,source,tag,content,author,imgurl,part from weatherdb.news a where a.title not in (select title from weather_user.news);

select count(*) from weatherdb.request_finger a where a.finger not in (select finger from weather_user.news_finger);
--258
insert into weather_user.news_finger(finger)
select finger from weatherdb.request_finger a where a.finger not in (select finger from weather_user.news_finger);

select count(*) from weatherdb.tjnews a where a.title not in (select title from weather_user.tjnews);
--37
insert into weather_user.tjnews (newsurl,title,categoryid,time,source,tag,content,author,imgurl,part)
select newsurl,title,categoryid,time,source,tag,content,author,imgurl,part from weatherdb.tjnews a where a.title not in (select title from weather_user.tjnews);



-- 目前核对到两个库之间的数据差别,差别不大,把重点的两个表的数据写过去就行

-- 接下来拷贝图片 + 修改spider脚本中的路径  +  启动定时任务

spider脚本修改项:
	1. 数据库连接
		self.db=pymysql.connect('172.86.140.47','work','123','weather_user',charset='utf8')
		改为:
		self.db=pymysql.connect('127.0.0.1','root','123456','weather_user',charset='utf8')
	2. 图片保存地址
		path= 'static/newsimages/'
		path= '/home/ubuntu/project/weather_client/static/newsimages/'
	3.日志文件保存路径
		with open('/home/tarena/CityWeather/log/
		with open('/home/ubuntu/logs/HexuWeather/spider/python_logs/
	4.修改crontab里爬虫文件路径为:
	/home/ubuntu/project/weather_spider
	和日志文件路径为:
	/home/ubuntu/logs/HexuWeather/spider/crontab_logs
	

	
	

	命令:
--linux下合并文件并覆盖
	cp -frap new/* test/
解释如下：
-f  强制覆盖，不询问yes/no（-i的默认的，即默认为交互模式，询问是否覆盖）
-r  递归复制，包含目录
-a  做一个备份，这里可以不用这个参数，我们可以先备份整个test目录
-p  保持新文件的属性不变
	
1、统计当前文件夹下文件的个数
ls -l |grep "^-"|wc -l

2、统计当前文件夹下目录的个数
ls -l |grep "^d"|wc -l
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	