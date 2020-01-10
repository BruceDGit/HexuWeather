#!/usr/bin/python3
#coding=utf-8
import sys
import time
from datetime import datetime
import requests
import json,pymysql

class GetForecastWeather(object):
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
        # print(data)
        self.insert_data(data)
    def insert_data(self,weather_text):
        datas = weather_text["HeWeather6"][0]
        for item in datas["daily_forecast"]:
            L = ((
                datas["basic"]["cid"],
                datas["basic"]["location"],
                datas["basic"]["parent_city"],
                datas["basic"]["admin_area"],
                datas["basic"]["cnty"],
                datetime.strptime(datas["update"]["loc"], '%Y-%m-%d %H:%M'),
                datetime.strptime(item["date"], '%Y-%m-%d'),
                '',
                '',
                '',
                '',
                item["tmp_max"],
                item["tmp_min"],
                item["cond_code_d"],
                item["cond_code_n"],
                item["cond_txt_d"],
                item["cond_txt_n"],
                item["wind_deg"],
                item["wind_dir"],
                item["wind_sc"],
                item["wind_spd"],
                item["hum"],
                item["pcpn"],
                item["pop"],
                item["pres"],
                item["uv_index"],
                item["vis"]
                ))
            ins = 'insert into w_city_7d_forecast (cid,location,parent_city,admin_area,cnty,update_loc,date,sr,ss,mr,ms,tmp_max,tmp_min,cond_code_d,cond_code_n,cond_txt_d,cond_txt_n,wind_deg,wind_dir,wind_sc,wind_spd,hum,pcpn,pop,pres,uv_index,vis) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            try:
                self.cursor.execute(ins,L)
                self.db.commit()
            except Exception as e:
                print(e)
                self.db.rollback()
    def run(self):
        for i in range(100,1800,100):
            city = 'CN10103' + str(i).zfill(4)
            self.get_html(self.url,city)
        self.cursor.close()
        self.db.close()
if __name__ == '__main__':
    try:
        api = GetForecastWeather()
        api.run()
        with open('/home/tarena/Bruce/CityWeather/111/log/weather_7days_insert.log' , 'a') as f:
            f.write('insert succeed at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            print('insert succeed at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    except Exception as e:
        with open('/home/tarena/Bruce/CityWeather/111/log/weather_7days_insert.log' , 'a') as f:
            f.write('error:{} {} \n'.format(e , datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
