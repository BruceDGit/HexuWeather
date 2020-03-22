import json

from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from user.models import User
def login(request):
    if request.method == 'GET':
        if 'username' in request.session and 'uid' in request.session:
            return JsonResponse({'code': 200, 'msg': 'ok'})
        if 'username' in request.COOKIES and 'uid' in request.COOKIES:
            #回写session
            request.session['username'] = request.COOKIES['username']
            request.session['uid'] = request.COOKIES['uid']
            return JsonResponse({'code': 200, 'msg':'ok'})

        return JsonResponse({'code': 400,'msg':'请您走正确的路'})
    elif request.method == 'POST':
        usermessage = request.body.decode()
        usermessage = json.loads(usermessage)
        username = usermessage['username']
        password = usermessage['password']
        user = User.objects.filter(name=username).order_by('-id')
        if not username:
            params = {
                'msg': "请输入用户名",
                'code':400
            }
            return JsonResponse(params)
        if not password:
            params = {
                'msg': "请输入密码",
                'code': 400
            }
            return JsonResponse(params)

        if not user:
            params = {
                'msg': "用户名不存在",
                'code': 400
            }
            return JsonResponse(params)
        if password != user[0].password_1:
            params = {
                'msg': "密码错误",
                'code': 400
            }
            return JsonResponse(params)
        request.session['username'] = username
        request.session['uid'] = user[0].id
        req = JsonResponse({'code': 200, 'msg': 'ok'})
        req.set_cookie('username', username)
        req.set_cookie('uid', user[0].id)
        return req


def register(request):
    if request.method == 'GET':
        return JsonResponse({'code': 400, 'msg': '请您走正确的路'})
    elif request.method == 'POST':
        usermessage = request.body.decode()
        usermessage = json.loads(usermessage)
        username = usermessage['username']
        password_1 = usermessage['password_1']
        password_2 = usermessage['password_2']
        email = usermessage['email']
        if password_1 != password_2:
            return JsonResponse({'code':400,'msg':'请输入相同的密码'})
        user = User.objects.filter(name=username)
        if user:
            return JsonResponse({'code': 400, 'msg': '您注册用户已存在'})
        try:
            user = User.objects.create(name=username, password_1=password_1,password_2=password_2,email=email)
        except Exception as e:
            print(e)
        return JsonResponse({'code':200,'msg':'注册成功'})

