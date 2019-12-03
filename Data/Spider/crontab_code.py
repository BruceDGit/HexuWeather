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

# 七天天气	一天更新一次
# WeatherSpider
0 10  * * * python3 /home/tarena/桌面/Github/WeatherSpider.py  >>/home/tarena/CityWeather/log/sevendaysweather_insert.log 2>&1

# 交通新闻	一天更新三次
# TrafficNewsSpider
15 9,14,18  * * * python3 /home/tarena/桌面/Github/WeatherSpider.py  >>/home/tarena/CityWeather/log/TrafficNews_insert.log 2>&1

# 天气新闻	一天更新三次
# WeatherNewsSpider
20 9,14,18  * * * python3 /home/tarena/桌面/Github/WeatherSpider.py  >>/home/tarena/CityWeather/log/WeatherNews_insert.log 2>&1

# 旅游新闻	一天更新两次
# TravelNewsSpider
15 12,18  * * * python3 /home/tarena/桌面/Github/WeatherSpider.py  >>/home/tarena/CityWeather/log/TravelNews_insert.log 2>&1


# 本地新闻	一天更新三次
# TjNewsSpider
10 9,14,18  * * * python3 /home/tarena/桌面/Github/WeatherSpider.py  >>/home/tarena/CityWeather/log/TjNews_insert.log 2>&1

# 新浪新闻	每两小时更新一次
# SinaNewsSpider
*/120 * * * * python3 /home/tarena/桌面/Github/WeatherSpider.py  >>/home/tarena/CityWeather/log/SinaNews_insert.log 2>&1

'''
