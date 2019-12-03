# -*- coding:utf-8 -*-
 ######################################################
#        > File Name: flask_client.py
#      > Author: Bruce
 #     > Mail: wayne_s@126.com
 #     > Created Time: Sat Nov  2 10:50:57 CST 2019
 ######################################################

from flask import Flask, send_file

app = Flask(__name__)

@app.route('/index')
def index():
    #首页
    return send_file('templates/index.html')

@app.route('/login')
def login():
    #登录
    return send_file('templates/login.html')

@app.route('/register')
def register():
    #注册
    return send_file('templates/register.html')
#
@app.route('/news')
def news():
    #资讯
    return send_file('templates/news.html')

@app.route('/news_info')
def news_info():
    #资讯
    return send_file('templates/news_info.html')

@app.route('/travel')
def travel():
    #旅游
    return send_file('templates/travel.html')

@app.route('/travel_info')
def travel_info():
    #旅游
    return send_file('templates/travel_info.html')

@app.route('/trip')
def trip():
    #出行
    return send_file('templates/trip.html')

@app.route('/weather')
def weather():
    #天气
    return send_file('templates/weather.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

