from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login', views.log_in, name ='login'),
    path('logout', views.log_out, name ='logout'),
    path('check_login', views.check_login, name ='check_login'),
]