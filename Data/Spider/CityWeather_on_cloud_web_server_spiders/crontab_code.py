"""
说明:
    step1: Linux命令行输入 'crontab -e' 进入vim编辑窗口;
    step2: 将下方代码复制粘贴到文档末尾, 保存退出即可.
"""


"""
# 实况天气	10-20分钟更新一次
# weather_now_insert
*/20 * * * * python3 /home/tarena/Bruce/CityWeather/111/weather_now_insert.py  >>/home/tarena/Bruce/CityWeather/111/crontab_log/weather_now_insert.log 2>&1

# 生活指数	每天更新3次，分别在8，11，18点左右更新
# weather_lifeindex_insert
27 9,12,19 * * * python3 /home/tarena/Bruce/CityWeather/111/weather_lifeindex_insert.py >>/home/tarena/Bruce/CityWeather/111/crontab_log/weather_lifeindex_insert.log 2>&1

# 今日天气	每小时更新一次
# weather_today_insert
15 * * * * python3 /home/tarena/Bruce/CityWeather/111/weather_today_insert.py >>/home/tarena/Bruce/CityWeather/111/crontab_log/weather_today_insert.log 2>&1

# 7日天气	每小时更新一次
# weather_7days_insert
35 * * * * python3 /home/tarena/Bruce/CityWeather/111/weather_7days_insert.py >>/home/tarena/Bruce/CityWeather/111/crontab_log/weather_7days_insert.log 2>&1
"""

'''

# 七天天气      一天更新一次
# WeatherSpider
0 10  * * * /home/ubuntu/anaconda3/bin/python3.6 /home/ubuntu/project/weather_spider/WeatherSpider.py  >>/home/ubuntu/logs/HexuWeather/spider/crontab_logs/sevendaysweather_insert.log 2>&1

# 交通新闻      一天更新三次
# TrafficNewsSpider
15 9,14,18  * * * /home/ubuntu/anaconda3/bin/python3.6 /home/ubuntu/project/weather_spider/TrafficNewsSpider.py  >>/home/ubuntu/logs/HexuWeather/spider/crontab_logs/TrafficNews_insert.log 2>&1

# 天气新闻      一天更新三次
# WeatherNewsSpider
20 9,14,18  * * * /home/ubuntu/anaconda3/bin/python3.6 /home/ubuntu/project/weather_spider/WeatherNewsSpider.py  >>/home/ubuntu/logs/HexuWeather/spider/crontab_logs/WeatherNews_insert.log 2>&1

# 旅游新闻      一天更新两次
# TravelNewsSpider
15 12,18  * * * /home/ubuntu/anaconda3/bin/python3.6 /home/ubuntu/project/weather_spider/TravelNewsSpider.py  >>/home/ubuntu/logs/HexuWeather/spider/crontab_logs/TravelNews_insert.log 2>&1

# 本地新闻      一天更新三次
# TjNewsSpider
10 9,14,18  * * * /home/ubuntu/anaconda3/bin/python3.6 /home/ubuntu/project/weather_spider/TjNewsSpider.py  >>/home/ubuntu/logs/HexuWeather/spider/crontab_logs/TjNews_insert.log 2>&1

# 新浪新闻      每两小时更新一次
# SinaNewsSpider
*/120 * * * * /home/ubuntu/anaconda3/bin/python3.6 /home/ubuntu/project/weather_spider/SinaNewsSpider.py  >>/home/ubuntu/logs/HexuWeather/spider/crontab_logs/SinaNews_insert.log 2>&1
'''

注意:
    1.这里有一个坑, 使用crontab执行定时任务的时候,由于crontab的执行环境和手动的不一样,手动执行的时候没问题,但是crontab就可能会报错
        常用解决办法如下:
            a. 不要用环境变量, 改用全路径, 例如pyhton3改为/home/ubuntu/anaconda3/bin/python3.6;
            b. 在执行命令前先cd到路径下, 把crontab命令改为 * * * * * cd /xxx/xxx/ && /xxx/python3 /xxx/xxx/python_code.py
