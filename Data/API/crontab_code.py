"""
说明:
    step1: Linux命令行输入 'crontab -e' 进入vim编辑窗口;
    step2: 将下方代码复制粘贴到文档末尾, 保存退出即可.
"""


"""
# 实况天气	每天更新一次
# weather_now_insert
27 8 * * * /home/ubuntu/anaconda3/bin/python3.6 /home/ubuntu/project/weather_spider/apis/weather_now_insert.py  >>/home/ubuntu/logs/HexuWeather/api/crontab_logs/weather_now_insert.log 2>&1

# 生活指数	每天更新一次
# weather_lifeindex_insert
27 9 * * * /home/ubuntu/anaconda3/bin/python3.6 /home/ubuntu/project/weather_spider/apis/weather_lifeindex_insert.py >>/home/ubuntu/logs/HexuWeather/api/crontab_logs/weather_lifeindex_insert.log 2>&1

# 今日天气	每天更新一次
# weather_today_insert
27 8 * * * /home/ubuntu/anaconda3/bin/python3.6 /home/ubuntu/project/weather_spider/apis/weather_today_insert.py >>/home/ubuntu/logs/HexuWeather/api/crontab_logs/weather_today_insert.log 2>&1

# 7日天气	每天更新一次
# weather_7days_insert
27 8 * * * /home/ubuntu/anaconda3/bin/python3.6 /home/ubuntu/project/weather_spider/apis/weather_7days_insert.py >>/home/ubuntu/logs/HexuWeather/api/crontab_logs/weather_7days_insert.log 2>&1
"""
