import requests,time,random,os
from fake_useragent import UserAgent
from lxml import etree
import pymysql

class WeatherImgSpider(object):
    def __init__(self):
        self.url = 'https://www.tianqi.com/tianjin/'
        self.headers = {'User-Agent': UserAgent().random}
        self.db = pymysql.connect(h'172.86.140.47','work','123','weather_user',charset='utf8')
        self.cur=self.db.cursor()

    def get_html(self,url):
        html= requests.get(url=url,headers=self.headers).content.decode('utf-8','ignore')
        return html


    #功能函数2: 解析函数
    def parse_xpfunc(self,xpath_bds,html):
        p=etree.HTML(html)
        r_list = p.xpath(xpath_bds)
        return r_list

    def parse_html(self):
        place_html = self.get_html(self.url)
        xpath_bds2='//div[@class="racitybox"]/div[@class="scenic_spot"]/ul/li//img/@src'
        xpath_bds1='//div[@class="racitybox"]/div[@class="scenic_spot"]/ul/li//div[@class="jingdian_name"]/text()'
        name_list = self.parse_xpfunc(xpath_bds1,place_html)[:10]
        img_list=self.parse_xpfunc(xpath_bds2,place_html)[:10]
        for i in range(10):
            l=[name_list[i],img_list[i]]
            print(l)
            self.insert_data(l)
            time.sleep(random.randint(0,2))

    def insert_data(self,l):
        try:
            ins='insert into weatherimgs (name,imgurl)values(%s,%s)'
            self.cur.execute(ins,l)
            self.db.commit()
            print("插入完成")
        except Exception as e:
            self.db.rollback()
            print(e)
	


    def run(self):
        self.parse_html()




if __name__ == '__main__':
    spider=WeatherImgSpider()
    spider.run()



