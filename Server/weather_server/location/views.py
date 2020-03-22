from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from location.GetLocation import *
# Create your views here.


def user_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return JsonResponse({'code': 200,'user_ip': ip})


def location_ip(request,ip):
    req = GetLocation(ip)
    location = req.result()
    location = '中国,天津,天津'
    return JsonResponse(
        {
            'code': 200,
            'location':location
        }
    )
