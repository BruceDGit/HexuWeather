from django.urls import path,include,re_path
import tour.views as views
urlpatterns = [
    re_path(r'(?P<location>.*)',views.tour)

]
