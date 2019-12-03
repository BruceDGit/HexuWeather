#!/usr/bin/python3
#coding=utf-8
import time
from datetime import datetime
import requests
import json,pymysql

class WeatherAPI(object):
    def __init__(self):
        self.url = 'https://free-api.heweather.net/s6/weather/now'
        self.db = pymysql.connect(
            host='localhost' ,
            port=3306 ,
            user='root' ,
            passwd='123456' ,
            db='weather' ,
            charset='utf8' ,
        )
        self.cursor = self.db.cursor()
    # 获取请求
    def get_html(self,url,city):
        params = {
            'location': '%s'%city ,
            'lang': 'zh-Hans' ,
            'unit': 'm' ,
            'key': '0dfc6d91f0224823bf107e283dd9b0b2'
        }
        html = requests.get(
            url=url , params=params
        ).content.decode('utf-8' , 'ignore')
        # print('html:', html)
        self.parse_html_json(html)
    # json解析
    def parse_html_json(self,html):
        data = json.loads(html)
        self.insert_data(data)
    def insert_data(self,weather_text):
        # print(weather_text)
        L = ((
            weather_text['HeWeather6'][0]['basic']['admin_area'],
            weather_text['HeWeather6'][0]['basic']['parent_city'],
            weather_text['HeWeather6'][0]['basic']['location'],
            weather_text['HeWeather6'][0]['now']['tmp'],
            weather_text['HeWeather6'][0]['update']['loc'][:10],
            datetime.now().weekday()+1,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')[-8:-1:1] ,
            ))
        ins = 'insert into realtime_weather (province,city,district,temperature,t_date,get_week,time) values (%s,%s,%s,%s,%s,%s,%s)'
        try:
            self.cursor.execute(ins,L)
            self.db.commit()
        except Exception as e:
            # print(e)
            self.db.rollback()
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
        with open('/home/tarena/Bruce/CityWeather/111/log/weather_now_insert.log' , 'a') as f:
            f.write('insert succeed at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            print('insert succeed at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    except Exception as e:
        with open('/home/tarena/Bruce/CityWeather/111/log/weather_now_insert.log' , 'a') as f:
            f.write('error:{} {} \n'.format(e , datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
