from django.urls import path,re_path
import location.views as views
urlpatterns = [
    path('user_ip',views.user_ip),
    re_path(r'location/(?P<ip>.*)', views.location_ip),
]