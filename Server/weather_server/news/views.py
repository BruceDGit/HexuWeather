import datetime

from django.db import connection
from django.shortcuts import render
from news.models import *

# Create your views here.
from django.http import HttpResponse,JsonResponse


def news(request,location):
    location = location.split(',')[-1]
    tour = request.GET.get('tour')
    city = request.GET.get('city')
    weather = request.GET.get('weather')
    banner = request.GET.get('banner')
    traffic = request.GET.get('traffic')
    recommendation = request.GET.get('recommendation')

    if weather:
        if weather and banner:
            n_id = []
            title = []
            img_src = []
            weather_list = Weather.objects.filter(categoryid=location)
            for i in range(3):
                n_id.append(i)
                title.append(weather_list[i].title)
                img_src.append(weather_list[i].imgurl)
            data = {
                'n_id': n_id,
                'title': title,
                'img_src':img_src
            }
            return JsonResponse({
                'code': 200,
                'data': data,
                'img_src':img_src
            })
        n_id = []
        title = []
        weather_list = Weather.objects.filter(categoryid=location)
        for i in range(6):
            n_id.append(i)
            title.append(weather_list[i].title)
        data = {
            'n_id': n_id,
            'title': title
        }
        return JsonResponse({
            'code': 200,
            'data': data
        })

    if city:
        if tour and city:
            # categoryid: 国内新闻
            # message_list = News.objects.filter(categoryid=location)
            message_list = TjNews.objects.filter()
            print('*'*45)
            print(message_list)
            n_id = []
            title = []
            for i in range(6):
                n_id.append(i)
                title.append(message_list[i].title)
            data = {
                'n_id': n_id,
                'title': title
            }
            return JsonResponse({
                'code': 200,
                'data': data
            })
        n_id = []
        title = []
        # message_list = News.objects.filter(categoryid=location)
        message_list = News.objects.filter()
        for i in range(12):
            n_id.append(i)
            title.append(message_list[i].title)
        data = {
            'n_id': n_id,
            'title': title

        }
        return JsonResponse({
            'code': 200,
            'data': data
        })

    if tour:
        if tour and city:
            # message_list = News.objects.filter(categoryid=location)
            message_list = News.objects.filter()
            n_id = []
            title = []
            for i in range(6):
                n_id.append(i)
                title.append(message_list[i].title)
            data = {
                'n_id': n_id,
                'title': title
            }
            return JsonResponse({
                'code': 200,
                'data': data
            })
        n_id = []
        title = []
        message_list = News.objects.all()
        for i in range(6):
            n_id.append(i)
            title.append(message_list[i].title)
        data = {
            'n_id': n_id,
            'title': title
        }
        return JsonResponse({
            'code': 200,
            'data': data
        })

    if traffic:
        n_id = []
        title = []
        img_src = []
        # traffic_list = Traffic.objects.filter(categoryid=location)
        traffic_list = Traffic.objects.filter()
        for i in range(3):
            n_id.append(i)
            title.append(traffic_list[i].title)
            img_src.append(traffic_list[i].imgurl)
        data = {
            'n_id': n_id,
            'title': title,
            'img_src': img_src
        }
        return JsonResponse({
            'code': 200,
            'data': data,
            'img_src': img_src
        })


def news_detail(request):
    new_id = request.GET.get('new_id')
    data = {}
    if new_id:
        try:
            news = News.objects.get(id=new_id)
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'data': '新闻不存在'
            })
        data['title'] = news.title
        data['categoryld'] = news.categoryid
        data['time'] = news.time
        data['source'] = news.source
        data['author'] = news.author
        data['tag'] = news.tag
        data['context'] = news.context
        data['imgurl'] = news.imgurl
        return JsonResponse({
            'code': 200,
            'data': data
        })


def today_news(request,location):
    with connection.cursor() as cur:
        sql = """
        select a.id, a.title, a.date
          from (select id, title, date from news where date > (now() - interval 1 day))a
          left join news_recommendation b
            on a.id = b.new_id
      order by a.id desc;
        """
        cur.execute(sql)
        # ((1, '中国人习以为常的地方 为何老外却说“了不得”？'), (2, '澳大利亚不依不饶：中国想在我们议会安插间谍'))
        message_tuple = cur.fetchall()
    n_id = []
    title = []
    date_ = []
    for item in message_tuple:
        n_id.append(item[0])
        title.append(item[1])
        date_.append(datetime.datetime.strftime(item[2], '%Y-%m-%d %H:%M:%S'))
    data = {
        'n_id': n_id,
        'title': title,
        'date':date_
    }
    return JsonResponse({
            'code': 200,
            'data': data
        })


def news_recommendation(request):
    new_id = request.GET.get('new_id')
    new_id_lst = [new_id for i in range(10)]
    with connection.cursor() as cur:
        sql = """
        select a.id, a.title
          from news a
         where a.id in (select reco_rank_1 news_id from news_recommendation where new_id = %s
                        union
                        select reco_rank_2 news_id from news_recommendation where new_id = %s
                        union
                        select reco_rank_3 news_id from news_recommendation where new_id = %s
                        union
                        select reco_rank_4 news_id from news_recommendation where new_id = %s
                        union
                        select reco_rank_5 news_id from news_recommendation where new_id = %s
                        union
                        select reco_rank_6 news_id from news_recommendation where new_id = %s
                        union
                        select reco_rank_7 news_id from news_recommendation where new_id = %s
                        union
                        select reco_rank_8 news_id from news_recommendation where new_id = %s
                        union
                        select reco_rank_9 news_id from news_recommendation where new_id = %s
                        union
                        select reco_rank_10 news_id from news_recommendation where new_id = %s
                        )
      order by a.date desc;
        """
        cur.execute(sql, new_id_lst)
        # ((1, '中国人习以为常的地方 为何老外却说“了不得”？'), (2, '澳大利亚不依不饶：中国想在我们议会安插间谍'))
        message_tuple = cur.fetchall()
    n_id = []
    title = []
    for item in message_tuple:
        n_id.append(item[0])
        title.append(item[1])
    data = {
        'n_id': n_id,
        'title': title
    }
    return JsonResponse({
        'code': 200,
        'data': data
    })
