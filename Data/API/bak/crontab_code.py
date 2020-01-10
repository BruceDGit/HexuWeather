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
