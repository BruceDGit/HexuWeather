#!/usr/bin/python3
#coding=utf-8
import time
from datetime import datetime
import requests
import json,pymysql

class WeatherAPI(object):
    def __init__(self):
        self.url = 'https://api.heweather.net/s6/weather/forecast'
        self.db = pymysql.connect(
            host='localhost' ,
            port=3306 ,
            user='root' ,
            passwd='123456' ,
            db='weather_user' ,
            charset='utf8' ,
        )
        self.cursor = self.db.cursor()
    # 获取请求
    def get_html(self,url,city):
        params = {
            'location': '%s'%city ,
            'lang': 'zh-Hans' ,
            'unit': 'm' ,
            'key': '4dcf0ac571c64e45ad7767a44f692902'
        }
        html = requests.get(
            url=url , params=params
        ).content.decode('utf-8' , 'ignore')
        self.parse_html_json(html)
    # json解析
    def parse_html_json(self,html):
        data = json.loads(html)
        self.insert_data(data)
    def insert_data(self,weather_text):
        L = ((
            weather_text['HeWeather6'][0]['basic']['admin_area'],
            weather_text['HeWeather6'][0]['basic']['parent_city'],
            weather_text['HeWeather6'][0]['basic']['location'],
            weather_text['HeWeather6'][0]['update']['loc'][:10],
            datetime.now().weekday()+1,
            weather_text['HeWeather6'][0]['daily_forecast'][0]['tmp_max'] ,
            weather_text['HeWeather6'][0]['daily_forecast'][0]['tmp_min'] ,
            weather_text['HeWeather6'][0]['daily_forecast'][0]['cond_txt_d'] ,
            weather_text['HeWeather6'][0]['daily_forecast'][0]['wind_dir'] ,
            weather_text['HeWeather6'][0]['daily_forecast'][0]['wind_sc'] ,
            ))
        ins = 'insert into today_weather (province,city,district,t_date,' \
              'get_week,temperature_max,temperature_min,weather,wind_direct,wind_strength)' \
              ' values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(ins,L)
        self.db.commit()
    def run(self):
        for i in range(100,1800,100):
            city = 'CN10103' + str(i).zfill(4)
            self.get_html(self.url,city)
        self.cursor.close()
        self.db.close()

if __name__ == '__main__':
    try:
        api = WeatherAPI()
        api.run()
        with open('/home/tarena/Bruce/CityWeather/111/log/weather_today_insert.log' , 'a') as f:
            f.write('insert succeed at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            print('insert succeed at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    except Exception as e:
        with open('/home/tarena/Bruce/CityWeather/111/log/weather_today_insert.log' , 'a') as f:
            f.write('error:{} {} \n'.format(e , datetime.now().strftime('%Y-%m-%d %H:%M:%S')))