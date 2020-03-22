from django.urls import path,include
import user.views as views
urlpatterns = [
    path('login',views.login),
    path('register',views.register)
]