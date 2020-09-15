from django.urls import path,include
from notice import views
from rest_framework import routers
urlpatterns = [
    path(r'api/get_notice_list/', views.get_notice_list,name='get_notice_list'),
    path(r'api/get_notice_count/', views.get_notice_count,name='get_notice_count'),
    path(r'api/mark_as_read/', views.mark_as_read,name='mark_as_read'),
    path(r'api/mark_all_as_read/', views.mark_all_as_read,name='mark_all_as_read'),
]
