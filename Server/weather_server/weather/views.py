import datetime

from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from weather.models import *
# Create your views here.


def weather(request, location):
    location = location.split(',')[-1]
    index = request.GET.get('index')
    now = request.GET.get('now')
    living_index = request.GET.get('living_index')
    temp24 = request.GET.get('temp24')
    wind_scale24 = request.GET.get('wind_scale24')
    forecast_7d = request.GET.get('forecast_7d')
    surrounding_weather = request.GET.get('surrounding_weather')
    if index:
        time = []
        temp = []
        now_weather = None
        temp_list = RealtimeWeather.objects.filter(city=location).order_by('-id')
        now_time = (datetime.datetime.now()).strftime("%H")
        for i in range(len(temp_list)):
            if now_time == temp_list[i].time.strftime("%H"):
                now_weather = temp_list[i].weather
                for j in range(i, i+5):
                    time.append(now_time)
                    temp.append(temp_list[j].temperature)
                    now_time = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%H")
                break
        temperature = {
            'time': now_time,
            'temp': temp
        }
        data = {
            'weather': now_weather,
            'temperature': temperature,
        }
        param = {
            'code': 200,
            'data': data
        }
        return JsonResponse(param)
    if now:
        now_weather = RealtimeWeather.objects.filter(city=location).order_by('-id')[0]
        today_weather = TodayWeather.objects.filter(city=location).order_by('-id')[0]
        wind = {
            'scale': today_weather.wind_direct,
            'direction': today_weather.wind_strength
        }
        data = {
            'weather':now_weather.weather,
            'temperature':now_weather.temperature,
            'wind':wind
        }
        return JsonResponse(
            {
                'code':200,
                'data':data
            }
        )
    if living_index:
        weather_life = WeatherLifeindex.objects.filter(city=location)[0]
        clothing = weather_life.dress_index
        uv = weather_life.uv_index
        car_washing = weather_life.carwash_index
        air_pollution_diffusion = weather_life.pm_index
        data = {
            'clothing':clothing,
            'uv':uv,
            'car_washing':car_washing,
            'air_pollution_diffusion':air_pollution_diffusion
        }
        return JsonResponse({
            'code':200,
            'data':data
        })
    # if temp24:
    #     time = []
    #     temperature = []
    #     temp_list = RealtimeWeather.objects.filter(city=location)
    #     now_time = (datetime.datetime.now()).strftime("%H")
    #     for i in range(len(temp_list)):
    #         if now_time in temp_list[i].time:
    #             for j in range(i, i + 24):
    #                 time.append(now_time)
    #                 temperature.append(temp_list[j].temperature)
    #                 now_time = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%H")
    #             break
    #     data = {
    #         'time': time,
    #         'temperature':temperature
    #     }
    #     return JsonResponse({
    #         'code': 200,
    #         'data': data
    #     })
    # if wind_scale24:
    #     time = []
    #     wind_list = []
    #     temp_list = RealtimeWeather.objects.filter(city=location).order_by('-id')
    #     now_time = (datetime.datetime.now()).strftime("%H")
    #     for i in range(len(temp_list)):
    #         if now_time in temp_list[i].time:
    #             for j in range(i, i + 24):
    #                 time.append(now_time)
    #                 wind_list.append(temp_list[j].temperature)
    #                 now_time = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%H")
    #             break
    #     data = {
    #         'time': time,
    #         'wind': wind_list
    #     }
    #     return JsonResponse({
    #         'code': 200,
    #         'data': data
    #     })
    if forecast_7d:
        date_list = []
        weather_list = []
        temperature_list = []
        wind_direction_list = []
        wind_scale_list = []
        target_day = None
        target_day_date = None
        # location_list = WCity7dForecast.objects.filter(parent_city=location).order_by('-id')
        location_list = WCity7dForecast.objects.filter(location=location).order_by('-id')
        # print('*' * 45)
        # print('test is ok')
        # print(location_list)
        # today = datetime.datetime.strftime(datetime.datetime.now(), '%Y/%m/%d')
        # today = datetime.datetime.strftime(datetime.datetime.now()+datetime.timedelta(days=-1), '%Y-%m-%d')
        today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        # print(today)
        for item in location_list:
            if today == str(item.date):
            # if today == item.date:
                print('*' * 45)
                print(today)
                print(str(item.date))
                print('*' * 80)
                print('test is ok')
                print(item.date)

                target_day = item
                print(type(target_day.date))
                print(target_day.date)
                target_day_date = target_day.date
                break
        print(type(target_day))
        for i in range(7):
            date_list.append(target_day.date.strftime('%m/%d'))
            # date_list.append(target_day_date.strftime('%m/%d'))
            weather_list.append(target_day.cond_txt_d)
            max_temp = target_day.tmp_max
            min_temp = target_day.tmp_min
            temp = str(max_temp) + '/' + str(min_temp)
            temperature_list.append(temp)
            wind_direction_list.append(target_day.wind_dir)
            wind_scale_list.append(target_day.wind_sc)
            today = datetime.datetime.strftime(datetime.datetime.now()+datetime.timedelta(days=1), '%Y/%m/%d')
            try:
                target_day = WCity7dForecast.objects.raw(
                    'select * from w_city_7d_forecast where parent_city=%s and date = %s order by id desc limit 1',[location, today])[0]
            except Exception as e:
                return JsonResponse({
                    'code': 400,
                    'data': 'error'
                })
        data = {
            'location': location_list,
            'weather': weather_list,
            'temperature': temperature_list,
            'wind_direction': wind_direction_list,
            'wind_scale': wind_scale_list
        }
        # data = serializers.serialize("json",data)
        return JsonResponse({
            'code':200,
            'data':data
        })

    if surrounding_weather:
        # district_list = []
        district_list = set()
        temperature_list = []
        weather_list = []
        city_list = TodayWeather.objects.filter(city=location).order_by('-id')
        for city in city_list:
            if city.district not in location:
                # district_list.append(city.district)
                district_list.add(city.district)
        district_list = list(district_list)
        for dis in district_list:
            #地区对象
            loc = TodayWeather.objects.filter(district=dis).order_by('-id')[0]
            max_temp = loc.temperature_max
            min_temp = loc.temperature_min
            temp = str(max_temp) + '/' + str(min_temp)
            temperature_list.append(temp)
            weather_list.append(loc.weather)
        data = {
            'location': district_list,
            'weather': weather_list,
            'temperature': temperature_list
        }
        return JsonResponse(
            {
                'code': 200,
                'data': data
            }
        )












