from django.db import models

# Create your models here.


class SevendaysWeather(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=16,verbose_name="姓名")
    datatime = models.CharField(max_length=12,verbose_name="时间")
    day01 = models.CharField(max_length=50)
    day02 = models.CharField(max_length=50)
    day03 = models.CharField(max_length=50)
    day04 = models.CharField(max_length=50)
    day05 = models.CharField(max_length=50)
    day06 = models.CharField(max_length=50)
    day07 = models.CharField(max_length=50)

    class Meta:
        db_table = 'sevendaysweather'
        unique_together = ("name", "datatime")


class SevendaysWeatherImage(models.Model):
    name = models.CharField(max_length=32,verbose_name='景点名称')
    imgurl = models.CharField(max_length=256,verbose_name='图片路径')

    class Meta:
        db_table = 'sevendaysweatherimage'


class News(models.Model):
    newsurl = models.CharField(max_length=256,verbose_name='链接')
    title = models.CharField(max_length=64,verbose_name="标题")
    categoryid = models.CharField(max_length=256,verbose_name='分类')
    time = models.CharField(max_length=64,verbose_name='新闻时间')
    source = models.CharField(max_length=64,verbose_name='来源网站')
    tag = models.CharField(max_length=64,verbose_name='新闻标签')
    context = models.TextField(verbose_name='正文')
    imgurl = models.CharField(max_length=512,verbose_name='图片链接')
    part = models.TextField(verbose_name='正文代码块')
    author = models.CharField(max_length=64, verbose_name='作者')

    class Meta:
        db_table = 'news'


class Traffic(models.Model):
    newsurl = models.CharField(max_length=256,verbose_name='链接')
    title = models.CharField(max_length=64,verbose_name="标题")
    categoryid = models.CharField(max_length=256,verbose_name='分类')
    time = models.CharField(max_length=64,verbose_name='新闻时间')
    source = models.CharField(max_length=64,verbose_name='来源网站')
    tag = models.CharField(max_length=64,verbose_name='新闻标签')
    context = models.TextField(verbose_name='正文')
    imgurl = models.CharField(max_length=512,verbose_name='图片链接')
    part = models.TextField(verbose_name='正文代码块')
    author = models.CharField(max_length=64, verbose_name='作者')

    class Meta:
        db_table = 'traffic'



class Weather(models.Model):
    newsurl = models.CharField(max_length=256,verbose_name='链接')
    title = models.CharField(max_length=64,verbose_name="标题")
    categoryid = models.CharField(max_length=256,verbose_name='分类')
    time = models.CharField(max_length=64,verbose_name='新闻时间')
    source = models.CharField(max_length=64,verbose_name='来源网站')
    tag = models.CharField(max_length=64,verbose_name='新闻标签')
    context = models.TextField(verbose_name='正文')
    imgurl = models.CharField(max_length=512,verbose_name='图片链接')
    part = models.TextField(verbose_name='正文代码块')
    author = models.CharField(max_length=64, verbose_name='作者')

    class Meta:
        db_table = 'weather'

class SpecialNews(models.Model):
    newsurl = models.CharField(max_length=256,verbose_name='链接')
    title = models.CharField(max_length=64,verbose_name="标题")
    categoryid = models.CharField(max_length=256,verbose_name='分类')
    time = models.CharField(max_length=64,verbose_name='新闻时z间')
    source = models.CharField(max_length=64,verbose_name='来源网站')
    tag = models.CharField(max_length=64,verbose_name='新闻标签')
    context = models.TextField(verbose_name='正文')
    imgurl = models.CharField(max_length=512,verbose_name='图片链接')
    part = models.TextField(verbose_name='正文代码块')
    author = models.CharField(max_length=64,verbose_name='作者')

    class Meta:
        db_table = 'special_news'


class NewsFinger(models.Model):
    finger = models.CharField(max_length=32, verbose_name='指纹')

    class Meta:
        db_table = 'news_finger'


class TjNews(models.Model):
    newsurl = models.CharField(max_length=256,verbose_name='链接')
    title = models.CharField(max_length=64,verbose_name="标题")
    categoryid = models.CharField(max_length=256,verbose_name='分类')
    time = models.CharField(max_length=64,verbose_name='新闻时间')
    source = models.CharField(max_length=64,verbose_name='来源网站')
    tag = models.CharField(max_length=64,verbose_name='新闻标签')
    content = models.TextField(verbose_name='正文')
    imgurl = models.CharField(max_length=512,verbose_name='图片链接')
    part = models.TextField(verbose_name='正文代码块')
    author = models.CharField(max_length=64, verbose_name='作者')

    class Meta:
        db_table = 'tjnews'


class TravelNews(models.Model):
    newsurl = models.CharField(max_length=256,verbose_name='链接')
    title = models.CharField(max_length=64,verbose_name="标题")
    categoryid = models.CharField(max_length=256,verbose_name='分类')
    time = models.CharField(max_length=64,verbose_name='新闻时间')
    source = models.CharField(max_length=64,verbose_name='来源网站')
    tag = models.CharField(max_length=64,verbose_name='新闻标签')
    content = models.TextField(verbose_name='正文')
    imgurl = models.CharField(max_length=512,verbose_name='图片链接')
    part = models.TextField(verbose_name='正文代码块')
    author = models.CharField(max_length=64, verbose_name='作者')

    class Meta:
        db_table = 'travelnews'

