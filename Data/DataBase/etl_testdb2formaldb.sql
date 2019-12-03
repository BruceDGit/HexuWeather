--------------------------------------------------------------
--数据初始化命令(将测试库已有数据导出至生产库. ps.需先将测试库数据备份出来)
--------------------------------------------------------------
desc news;
insert into weather_user.news(id,newsurl,title,categoryid,time,source,tag,context,imgurl,part,author)
	 select id,newsurl,title,categoryid,time,source,tag,context,imgurl,part,author
	   from weather.news;
desc news_finger;
insert into weather_user.news_finger(id,finger)
	 select id,finger
	   from weather.news_finger;
desc realtine_weather;
insert into weather_user.realtine_weather(id,province,city,district,temperature,weather,t_date,get_week,time)
	 select id,province,city,district,temperature,weather,t_date,get_week,time
	   from weather.realtine_weather;
desc sevendaysweather;
insert into weather_user.sevendaysweather(id,name,datatime,day01,day02,day03,day04,day05,day06,day07)
	 select id,name,datatime,day01,day02,day03,day04,day05,day06,day07
	   from weather.sevendaysweather;
desc sevendaysweatherimage;
insert into weather_user.sevendaysweatherimage(id,name,imgurl)
	 select id,name,imgurl
	   from weather.sevendaysweatherimage;
desc special_news;
insert into weather_user.special_news(id,newsurl,title,categoryid,time,source,tag,context,imgurl,part,author)
	 select id,newsurl,title,categoryid,time,source,tag,context,imgurl,part,author
	   from weather.special_news;
desc tjnews;
insert into weather_user.tjnews(id,newsurl,title,categoryid,time,source,tag,content,imgurl,part,author)
	 select id,newsurl,title,categoryid,time,source,tag,content,imgurl,part,author
	   from weather.tjnews;

desc today_weather;
insert into weather_user.today_weather(id,province,city,district,t_date,get_week,temperature_max,temperature_min,weather,wind_direct,wind_strength)
	 select id,province,city,district,t_date,get_week,temperature_max,temperature_min,weather,wind_direct,wind_strength
	   from weather.today_weather;
desc traffic;
insert into weather_user.traffic(id,newsurl,title,categoryid,time,source,tag,context,imgurl,part,author)
	 select id,newsurl,title,categoryid,time,source,tag,context,imgurl,part,author
	   from weather.traffic;

desc travelnews;
insert into weather_user.travelnews(id,newsurl,title,categoryid,time,source,tag,content,imgurl,part,author)
	 select id,newsurl,title,categoryid,time,source,tag,content,imgurl,part,author
	   from weather.travelnews;
desc user;
desc w_city_7d_forecast;
insert into weather_user.w_city_7d_forecast(id,cid,location,parent_city,admin_area,cnty,update_loc,date,sr,ss,mr,ms,tmp_max,tmp_min,cond_code_d,cond_code_n,cond_txt_d,cond_txt_n,wind_deg,wind_dir,wind_sc,wind_spd,hum,pcpn,pop,pres,uv_index,vis)
	 select id,cid,location,parent_city,admin_area,cnty,update_loc,date,sr,ss,mr,ms,tmp_max,tmp_min,cond_code_d,cond_code_n,cond_txt_d,cond_txt_n,wind_deg,wind_dir,wind_sc,wind_spd,hum,pcpn,pop,pres,uv_index,vis
	   from weather.w_city_7d_forecast;
desc weather;
insert into weather_user.weather(id,newsurl,title,categoryid,time,source,tag,context,imgurl,part,author)
	 select id,newsurl,title,categoryid,time,source,tag,context,imgurl,part,author
	   from weather.weather;
desc weather_lifeindex;
insert into weather_user.weather_lifeindex(id,province,city,district,t_date,dress_index,uv_index,carwash_index,pm_index)
	 select id,province,city,district,t_date,dress_index,uv_index,carwash_index,pm_index
	   from weather.weather_lifeindex;


