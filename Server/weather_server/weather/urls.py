from django.urls import path,re_path
import weather.views as views
urlpatterns = [
    re_path(r'(?P<location>.*)',views.weather)

]
