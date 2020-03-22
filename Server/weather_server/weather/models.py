from django.db import models

# Create your models here.


class RealtimeWeather(models.Model):
    province = models.CharField(max_length=20,verbose_name="省份")
    city = models.CharField(max_length=20,verbose_name="城市")
    district = models.CharField(max_length=20,verbose_name="区")
    temperature = models.IntegerField(verbose_name="温度")
    weather = models.CharField(max_length=20,verbose_name='天气')
    t_date = models.DateField(verbose_name='日期')
    get_week = models.CharField(max_length=10,verbose_name="具体星期")
    time = models.TimeField(verbose_name='时间')

    class Meta:
        db_table = 'realtine_weather'


class TodayWeather(models.Model):
    province = models.CharField(max_length=20, verbose_name="省份")
    city = models.CharField(max_length=20, verbose_name="城市")
    district = models.CharField(max_length=20, verbose_name="区")
    t_date = models.DateField(verbose_name='日期')
    get_week = models.IntegerField(verbose_name='星期')
    temperature_max = models.IntegerField(verbose_name='最高温度')
    temperature_min = models.IntegerField(verbose_name='最低温度')
    weather = models.CharField(max_length=20,verbose_name='天气')
    wind_direct = models.CharField(max_length=40,verbose_name='风向')
    wind_strength = models.CharField(max_length=20,verbose_name='风力')

    class Meta:
        db_table = 'today_weather'


class WeatherLifeindex(models.Model):
    province = models.CharField(max_length=20, verbose_name="省份")
    city = models.CharField(max_length=20, verbose_name="城市")
    district = models.CharField(max_length=20, verbose_name="区")
    t_date = models.DateField(verbose_name='日期')
    dress_index = models.CharField(max_length=100,verbose_name='穿衣指数')
    uv_index = models.CharField(max_length=100,verbose_name='紫外线指数')
    carwash_index = models.CharField(max_length=100,verbose_name='洗车指数')
    pm_index = models.CharField(max_length=100,verbose_name='PM指数')

    class Meta:
        db_table = 'weather_lifeindex'


class WCity7dForecast(models.Model):
    cid = models.CharField(max_length=16, verbose_name='城市id')
    location = models.CharField(max_length=64, verbose_name='地区')
    parent_city = models.CharField(max_length=64, verbose_name='城市')
    admin_area = models.CharField(max_length=64, verbose_name='省')
    cnty = models.CharField(max_length=64, verbose_name='国家')
    update_loc = models.DateTimeField(verbose_name='更新时间')
    date = models.DateField(verbose_name='预报日期')
    sr = models.CharField(max_length=8, verbose_name='日出时间',default='')
    ss = models.CharField(max_length=8, verbose_name='日落时间',default='')
    mr = models.CharField(max_length=8, verbose_name='月出时间',default='')
    ms = models.CharField(max_length=8, verbose_name='月升时间',default='')
    tmp_max = models.CharField(max_length=4, verbose_name='最高温度')
    tmp_min = models.CharField(max_length=4, verbose_name='最低温度')
    cond_code_d = models.CharField(max_length=16, verbose_name='白天天气状况代码')
    cond_code_n = models.CharField(max_length=16, verbose_name='夜晚天气状况代码')
    cond_txt_d = models.CharField(max_length=64, verbose_name='白天天气状况描述')
    cond_txt_n = models.CharField(max_length=64, verbose_name='夜晚天气状况描述')
    wind_deg = models.CharField(max_length=8, verbose_name='风向360角度')
    wind_dir = models.CharField(max_length=8, verbose_name='风向')
    wind_sc = models.CharField(max_length=8, verbose_name='风力')
    wind_spd = models.CharField(max_length=8, verbose_name='风速')
    hum = models.CharField(max_length=16, verbose_name='相对温度')
    pcpn = models.CharField(max_length=16, verbose_name='降水量')
    pop = models.CharField(max_length=16, verbose_name='降水概率')
    pres = models.CharField(max_length=16, verbose_name='⼤⽓压强')
    uv_index = models.CharField(max_length=16, verbose_name='紫外线强度指数')
    vis = models.CharField(max_length=16, verbose_name='能⻅度，单位：公⾥')

    class Meta:
        db_table = 'w_city_7d_forecast'


