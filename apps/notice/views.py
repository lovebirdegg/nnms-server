# @Time    : 2020/7/24 13:02
# @Author  : liuchao
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes


from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse,FileResponse,JsonResponse

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_xops.basic import XopsResponse
from rest_xops.code import *
from django.db.models import Q
from notifications.signals import notify
from notifications.models import Notification


from .serializers import *

import time
import hashlib
import requests
import json


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated])
def get_notice_count(request):
    #获取消息数量
    username = request.user.username
    unread_list = request.user.notifications.unread()
    read_list = request.user.notifications.read()
    unread_count = len(unread_list)
    read_count = len(read_list)

    result = {
        "unread_count":unread_count,
        "read_count":read_count
    }
    return JsonResponse(result,json_dumps_params={'ensure_ascii':False},safe=False)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated])
def get_notice_list(request):
    #取得消息列表
    print(request.GET)
    username = request.user.username
    notice_list = []
    if(request.GET['notice_type'] == '1'):#未读
        notice_list = request.user.notifications.unread()
    if(request.GET['notice_type'] == '0'):#已读
        notice_list = request.user.notifications.read()
    serializer_data = NotificationSerializer(instance=notice_list,many=True)  #可允许多个
    count = len(notice_list)
    result = {
        "count":count,
        "results":serializer_data.data
    }
    return JsonResponse(result,json_dumps_params={'ensure_ascii':False},safe=False)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated])
def mark_as_read(request):
    #标记单挑已读
    username = request.user.username
    print(request.data)
    notice_id = request.data['id']
    Notification.objects.get(pk=notice_id).mark_as_read()
    result = {
        "code":0,
        "message":''
    }
    return JsonResponse(result,json_dumps_params={'ensure_ascii':False},safe=False)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated])
def mark_all_as_read(request):
    #标记所有已读
    username = request.user.username
    unread_list = request.user.notifications.unread()
    unread_list.mark_all_as_read()
    result = {
        "code":0,
        "message":''
    }
    return JsonResponse(result,json_dumps_params={'ensure_ascii':False},safe=False)