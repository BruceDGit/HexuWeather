import re,time,pymysql,requests,random
from datetime import datetime

from lxml import etree

class WeatherSpider(object):
    def __init__(self):
        self.url='https://www.tianqi.com/tianjin/'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.time=time.localtime()
        self.db = pymysql.connect('172.86.140.47','work','123','weather_user',charset='utf8')
        self.cur=self.db.cursor()


    # 功能函数1: 获取html函数
    def get_html(self,url):
        html= requests.get(url=url,headers=self.headers).content.decode('utf-8','ignore')
        return html


    #功能函数2: 解析函数
    def parse_refunc(self,re_bds,html):
        p = re.compile(re_bds,re.S)
        r_list = p.findall(html)
        return r_list

    def parse_xpfunc(self,xpath_bds,html):
        p=etree.HTML(html)
        r_list = p.xpath(xpath_bds)
        return r_list


    def parse_html(self):
        place_html = self.get_html(self.url)
        xpath_bds1='//div[@class="racitybox"]/div[@class="scenic_spot"]/ul/li//div[@class="jingdian_name"]/text()'
        xpath_bds2='//div[@class="racitybox"]/div[@class="scenic_spot"]/ul/li//a/@href'
        name_list = self.parse_xpfunc(xpath_bds1,place_html)[:10]
        a_list=self.parse_xpfunc(xpath_bds2,place_html)[:10]
        i=0
        for link in a_list:
            w_url=self.url+link[9:]
            w_html=self.get_html(w_url)
            seven_day=self.parse_two_page(w_html)
            nowtime=str(self.time.tm_year)+'-'+str(self.time.tm_mon)+'-'+str(self.time.tm_mday)
            seven_day[:0]=(name_list[i],nowtime)
            i += 1
            self.insert_data(seven_day)
            time.sleep(random.randint(0,2))


    def insert_data(self,seven_day):
        try:
            ins='insert into sevendaysweather (name,datatime,day01,day02,day03,day04,day05,day06,day07) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            self.cur.execute(ins,seven_day)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)

    #解析二级页面的函数
    def parse_two_page(self,w_html):
        re_bds='<ul class="scroll_content clearfix">\s+(.*?)\s+</ul>'
        big_list=self.parse_refunc(re_bds,w_html)
        str="".join(big_list)
        p=re.compile('<li>\s+<p>(.*?)</p>\s+<h3>(.*?)</h3>.*?<div class="weather">(.*?)</div>\s+<div class="temp">(.*?)</div>\s+</li>',re.S)
        data_list=p.findall(str)[:7]
        seven_day=[]
        for day in data_list:
            day_weather=",".join(list(day))
            seven_day.append(day_weather)
        return seven_day

    def run(self):
        self.parse_html()


if __name__ == '__main__':
    spider = WeatherSpider()
    spider.run()
    try:
        with open('/home/tarena/CityWeather/log/sevendaysweather_insert.log', 'a') as f:
            f.write('insert succeed at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            print('insert succeed at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    except Exception as e:
        with open('/home/tarena/CityWeather/log/sevendaysweather_insert.log', 'a') as f:
            f.write('error:{} {} \n'.format(e, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))




'''
<li>\s+<p>星期五</p>\s+<h3>11月15日</h3>
<img src="//static.tianqistatic.com/static/wap2018/ico2/b0.png" alt="" width="42px" height="42px"/>
<div class="weather">晴</div>
<div class="temp">2℃~11℃</div>
</li>
'''