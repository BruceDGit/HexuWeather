from django.shortcuts import render
from django.http import JsonResponse
from news.models import SevendaysWeather,SevendaysWeatherImage
# Create your views here.
def tour(request,location):
    surrounding_weather = request.GET.get('surrounding_weather')
    top10 = request.GET.get('top10')
    weather_info = request.GET.get('weather_info')
    scenic_site_id = request.GET.get('scenic_site_id')

    if surrounding_weather:
        tour_list = SevendaysWeather.objects.all().order_by('-id')
        location_list = []
        temperature_list = []
        weather_list = []
        for i in range(5):
            location_list.append(tour_list[i].name)
            temperature_list.append(tour_list[i].day01.split(',')[3].strip())
            weather_list.append(tour_list[i].day01.split(',')[2].strip())
        data = {
            'location': location_list,
            'weather': weather_list,
            'temperature': temperature_list
        }
        return JsonResponse(
            {
                'code': 200,
                'data': data
            }
        )
    if top10:
        top10_list = SevendaysWeather.objects.all().order_by('-id')
        top10_img_list = SevendaysWeatherImage.objects.all().order_by('-id')
        scenic_site_id_list = []
        scenic_site_name_list = []
        img_src = []
        for i in range(10):
            scenic_site_id_list.append(i)
            scenic_site_name_list.append(top10_list[i].name)
        for name in scenic_site_name_list:
            for img in top10_img_list:
                if name == img.name:
                    img_src.append(img.imgurl)
        data = {
            'scenic_site_id': scenic_site_id_list,
            'scenic_site_name': scenic_site_name_list,
            'img_src': img_src
        }
        return JsonResponse(
            {
                'code': 200,
                'data': data
            }
        )
    if weather_info and scenic_site_id:
        # scenic_site_id = int(scenic_site_id)
        week_list = []
        date_list = []
        weather_list = []
        temperature_list = []
        tour_target = SevendaysWeather.objects.filter(name=scenic_site_id).order_by('-id')[0]
        # print('*'*45)
        # print(tour_target)
        week_list.append(tour_target.day01.split(',')[0].strip())
        week_list.append(tour_target.day02.split(',')[0].strip())
        week_list.append(tour_target.day03.split(',')[0].strip())
        week_list.append(tour_target.day04.split(',')[0].strip())
        week_list.append(tour_target.day05.split(',')[0].strip())
        week_list.append(tour_target.day06.split(',')[0].strip())
        week_list.append(tour_target.day07.split(',')[0].strip())

        date_list.append(tour_target.day01.split(',')[1].strip())
        date_list.append(tour_target.day02.split(',')[1].strip())
        date_list.append(tour_target.day03.split(',')[1].strip())
        date_list.append(tour_target.day04.split(',')[1].strip())
        date_list.append(tour_target.day05.split(',')[1].strip())
        date_list.append(tour_target.day06.split(',')[1].strip())
        date_list.append(tour_target.day07.split(',')[1].strip())

        weather_list.append(tour_target.day01.split(',')[2].strip())
        weather_list.append(tour_target.day02.split(',')[2].strip())
        weather_list.append(tour_target.day03.split(',')[2].strip())
        weather_list.append(tour_target.day04.split(',')[2].strip())
        weather_list.append(tour_target.day05.split(',')[2].strip())
        weather_list.append(tour_target.day06.split(',')[2].strip())
        weather_list.append(tour_target.day07.split(',')[2].strip())

        temperature_list.append(tour_target.day01.split(',')[3].strip())
        temperature_list.append(tour_target.day02.split(',')[3].strip())
        temperature_list.append(tour_target.day03.split(',')[3].strip())
        temperature_list.append(tour_target.day04.split(',')[3].strip())
        temperature_list.append(tour_target.day05.split(',')[3].strip())
        temperature_list.append(tour_target.day06.split(',')[3].strip())
        temperature_list.append(tour_target.day07.split(',')[3].strip())
        data = {
            'week': week_list,
            'date': date_list,
            'weather': weather_list,
            'temperature': temperature_list
        }
        return JsonResponse(
            {
                'code': 200,
                'data': data
            }
        )



