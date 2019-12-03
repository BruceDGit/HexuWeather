from queue import Queue

import requests,time,random,re,pymysql,os,gzip
from hashlib import md5
from lxml import etree
from fake_useragent import UserAgent
from datetime import datetime

class NewsSpider(object):
    def __init__(self):
        self.url = 'https://news.sina.com.cn/'
        self.headers = {'User-Agent':UserAgent().random}
        self.db=pymysql.connect('172.86.140.47','work','123','weather_user',charset='utf8')
        self.cur=self.db.cursor()
        self.one_q = Queue()
        self.two_q = Queue()

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

    # 5. 插入指纹函数
    def insert_finger(self,finger):
        ins='insert into news_finger values(%s)'
        self.cur.execute(ins,[finger])
        self.db.commit()

    # 6. 插入新闻内容
    def insert_news(self,all_list):
        # 插入'\链接\标题\分类\时间\来源\关键词\正文\作者\图片链接'
        ins='insert into news (newsurl,title,categoryid,time,source,tag,context,author,imgurl,part) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self.cur.execute(ins, all_list)
            self.db.commit()
            # print("插入成功")
        except Exception as e:
            self.db.rollback()
            print(e)

    # 7. 获取新浪新闻链接
    # 获取不同分类的新闻链接
    def get_news_link(self):
        page_html = self.get_html(self.url)
        # 所有国内(13)
        l1_bds = '//div[@id="blk_gnxw_01"]//a/@href'
        list1 = self.xpath_func(page_html, l1_bds)[:-1]
        # 所有国际(11)
        l2_bds = '//ul[@id="blk_gjxw_011"]//a/@href'
        list2 = self.xpath_func(page_html, l2_bds)
        # 所有财经等(19)
        l3_bds = '//ul[@id="blk_cjkjqcfc_011"]//a/@href'
        list3 = self.xpath_func(page_html, l3_bds)
        # 所有体育等(28)
        l4_bds = '//ul[@id="blk_lctycp_011"]//a/@href'
        list4 = self.xpath_func(page_html, l4_bds)
        nlink_list = list1 + list2 + list3 + list4
        for i in nlink_list:
            self.one_q.put(i)


    # 解析新闻链接主页
    def parse_sina_link(self, nlink_list):
        while True:
            try:
            m = md5()
            m.update(nlink.encode())
            finger = m.hexdigest()
            if not self.is_news_exist(finger):
                # 判断链接是否为新闻,不是则跳过
                all_list = self.parse_sina_news_page(nlink)
                if all_list:
                    self.insert_news(all_list)
                    self.insert_finger(finger)
                    print("已插入")
                    time.sleep(random.uniform(0, 1))
                else:
                    continue
            else:
                print("当前为最新")
                break

    # 解析新闻主页
    def parse_sina_news_page(self, nlink):
        html = self.get_html(nlink)
        # 新闻字段解析式
        category_bds = "//div[@class='channel-path']/a/text()"
        title_bds = "//h1[@class='main-title']/text()"
        source_bds = "//div[@class='date-source']//a/text()|//div[@class='date-source']/span[2]/text()"
        time_bds="//div[@class='date-source']/span[1]/text()"
        tag_bds = "//div[@class='keywords']/a/text()"
        news_bds = "//div[@class='article'] /p/text()"
        img_bds = "//div[@class='article']/div[@class='img_wrapper']/img/@src"
        part_bds='//div[@class="article"]'
        all_list = [nlink]
        # 获取新闻标题
        title_list = self.xpath_func(html, title_bds)
        if len(title_list) > 0:
            title = title_list[0].strip()
            all_list.append(title)
            # 获取新闻分类
            category = self.xpath_func(html, category_bds)[0].strip()
            all_list.append(category)
            # 获取新闻时间
            newstime = self.xpath_func(html, time_bds)[0].strip()
            all_list.append(newstime)
            # 获取新闻来源
            source = self.xpath_func(html, source_bds)[0].strip()
            all_list.append(source)
            # 获取新闻关键词
            tag = ','.join(self.xpath_func(html, tag_bds))
            all_list.append(tag)
            # 获取新闻正文
            text=self.xpath_func(html, news_bds)
            content = '\n'.join(text[:-1])
            all_list.append(content)
            # 添加作者
            all_list.append("Null")
            # 获取新闻代码块
            part_str = self.xpath_func(html, part_bds)[0]
            part=etree.tostring(part_str, encoding='utf-8').decode()
            # 获取新闻图片链接
            img_list = self.xpath_func(html, img_bds)
            imgurl_list=[]
            if len(img_list) > 0:
                for img in img_list:
                    imgurl=self.save_img(img)
                    p='src=".*?"'
                    part=re.sub(p,imgurl,part)
                    imgurl_list.append(imgurl)
            else:
                imgurl_list = ['Null']
            all_list.append(','.join(imgurl_list))
            all_list.append(part)

            print(len(all_list))
            return all_list
        else:
            return False

    # 10. 入口函数
    def run(self):
        #爬取新闻
        self.get_news_link()


if __name__ == '__main__':
    spider=NewsSpider()
    spider.run()
    try:
        with open('./log/SinaNews_insert.log', 'a') as f:
            f.write('insert succeed at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            print('insert succeed at {} \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    except Exception as e:
        with open('./log/SinaNews_insert.log', 'a') as f:
            f.write('error:{} {} \n'.format(e, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))





