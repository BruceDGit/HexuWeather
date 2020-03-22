from django.urls import path,include,re_path
import news.views as views
urlpatterns = [
    re_path(r'^detail$', views.news_detail),
    re_path(r'^recommendation$', views.news_recommendation),
    re_path(r'today/(?P<location>.*)', views.today_news),
    re_path(r'(?P<location>.*)', views.news) 
]
