import requests,time,random,pymysql
from hashlib import md5
from lxml import etree
from fake_useragent import UserAgent
from datetime import datetime

class WeatherNewsSpider(object):
    def __init__(self):
        self.weather_url='http://news.enorth.com.cn/tj/fwkx/tianqixinxi/'
        self.headers = {'User-Agent':UserAgent().random}
        self.db=pymysql.connect('172.86.140.47','work','123','weather_user',charset='utf8')
        self.cur=self.db.cursor()
        self.i =0

    # 1. 请求
    def get_html(self,url):
        html = requests.get(url=url,headers=self.headers).content.decode('utf-8','ignore')
        return html

    # 2. xpath解析
    def xpath_func(self,html,xpath_bds):
        p = etree.HTML(html)
        r_list = p.xpath(xpath_bds)
        return r_list

    # 3. 下载图片
    def save_img(self,img):
        if not img.startswith('http'):
            url='http:'+img
        else:
            url=img
        html= requests.get(url=url,headers=self.headers).content
        path= './static/newsimages/'
        imgurl=img.split('/')[-1]
        filename = path+imgurl
        with open(filename,'wb')as f:
            f.write(html)
        return 'src="'+'/static/newsimages/'+imgurl+'"'

    # 4. 判断新闻是否已经爬取
    def is_news_exist(self,finger):
        sel='select finger from news_finger where finger=%s'
        res = self.cur.execute(sel,[finger])
        if res:
            return True

    # # 5. 插入指纹函数
    # def insert_finger(self,finger):
    #     ins='insert into news_finger values(%s)'
    #     self.cur.execute(ins,[finger])
    #     self.db.commit()


    # 8. 插入天气新闻内容
    def insert_weather_news(self,all_list):
        # 插入'\链接\标题\分类\时间\来源\关键词\正文\作者\图片链接'
        ins='insert into weather (newsurl,title,categoryid,time,source,tag,context,author,imgurl,part) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self.cur.execute(ins, all_list)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)

    # 8. 获取天气新闻链接
    def get_weather_link(self):
        response = requests.get(url=self.weather_url, headers=self.headers)
        response.encoding = "gbk"
        html = response.text
        xpath_bds = '//tr[@valign="top"]//table//a/@href'
        nlink_list = self.xpath_func(html, xpath_bds)
        print(nlink_list)
        for nlink in nlink_list:
            m = md5()
            m.update(nlink.encode())
            finger = m.hexdigest()
            if not self.is_news_exist(finger):
                # 判断链接是否为新闻,不是则跳过
                all_list = self.parse_weather_news_page(nlink)
                if all_list:
                    self.insert_weather_news(all_list)
                    # self.insert_finger(finger)
                    self.i += 1
                    time.sleep(random.uniform(0, 1))
                else:
                    continue
            else:
                print("当前为最新")
                break

    # 解析天气新闻页面
    def parse_weather_news_page(self, nlink):
        response = requests.get(nlink, headers=self.headers)
        response.encoding = "gbk"
        html = response.text
        # 新闻字段解析式
        title_bds = '//*[@id="title"]//h2/text()'
        source_bds = "//*[@id='title']/div[2]/p/span[1]/text()"
        time_bds = "//*[@id='title']/div[2]/p/span[4]/text()"
        news_bds = "//*[@id='article']/div[2]/p/text()"
        author_bds = "//*[@id='title']/div[2]/p/span[2]/text()"
        # img_bds =''
        part_bds = "//div[@class='content']"
        all_list = [nlink]
        # 获取新闻标题
        title_list = self.xpath_func(html, title_bds)
        if len(title_list) > 0:
            title = title_list[0].strip()
            all_list.append(title)
            # 获取新闻分类
            all_list.append('天气')
            # 获取新闻时间
            newstime = self.xpath_func(html, time_bds)[0].strip()
            all_list.append(newstime)
            # 获取新闻来源
            source_list = self.xpath_func(html, source_bds)[0]
            source = source_list.split(" ")[-1].strip()
            all_list.append(source)
            # 获取新闻关键词
            tag = 'Null'
            all_list.append(tag)
            # 获取新闻正文
            text = self.xpath_func(html, news_bds)
            content = '\n'.join(text)
            all_list.append(content)
            # 添加作者
            author_list = self.xpath_func(html, author_bds)[0]
            author = author_list.split("：")[-1].strip()
            all_list.append(author)
            # 获取新闻代码块
            part_str = self.xpath_func(html, part_bds)[0]
            part = etree.tostring(part_str, encoding='utf-8').decode()
            # 获取新闻图片链接
            # img_list = []#self.xpath_func(html, img_bds)
            # imgurl_list = []
            # if len(img_list) > 0:
            #     for img in img_list:
            #         imgurl = self.save_img(img)
            #         p = 'src=".*?"'
            #         part = re.sub(p, imgurl, part)
            #         imgurl_list.append(imgurl)
            # else:
            #     imgurl_list = ['Null']
            # all_list.append(','.join(imgurl_list))
            all_list.append('Null')
            all_list.append(part)
            return all_list
        else:
            return False

    # 10. 入口函数
    def run(self):
        self.get_weather_link()

if __name__ == '__main__':
    spider=WeatherNewsSpider()
    spider.run()
    try:
        with open('/home/tarena/CityWeather/log//WeatherNews_insert.log', 'a') as f:
            f.write('insert succeed at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            print('insert succeed at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    except Exception as e:
        with open('/home/tarena/CityWeather/log//WeatherNews_insert.log', 'a') as f:
            f.write('error:{} {} \n'.format(e, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))




