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

import time
import hashlib
import requests


def get_headers(username):
    token = 'b4e6aba8-d242-11ea-ad60-8c8590535803'
    appname='eee'
    timestamp = str(time.time())[:10]
    ori_str = timestamp + token
    signature = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
    headers = dict(signature=signature, timestamp=timestamp, appname=appname, username=username)

    return headers
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated])
def workflow_test(request):
    # get
    print(request.GET["id"])
    workflow_id = request.GET["id"]
    username = request.user.username
    print(username)
    headers = get_headers(username)
    get_data = dict(per_page=20, category='all')
    # r = requests.get('http://127.0.0.1:8080/api/v1.0/workflows', headers=headers, params=get_data)
    # result = r.json()
    # response.write(result)
    r1 = requests.get('http://127.0.0.1:8080/api/v1.0/workflows/{}/init_state'.format(workflow_id), headers=headers, params=get_data)
    result1 = r1.json()
    return JsonResponse(result1,json_dumps_params={'ensure_ascii':False},safe=False)

def get_workflows(request):
    #获取可申请的工作流
    username = request.user.username
    headers = get_headers(username)
    get_data = dict(per_page=20, category='all')
    r = requests.get('http://127.0.0.1:8080/api/v1.0/workflows', headers=headers, params=get_data)
    result = r.json()
    return JsonResponse(result,json_dumps_params={'ensure_ascii':False},safe=False)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated])
def new_ticket(request):
    #新建工单
    username = request.user.username
    headers = get_headers(username)
    # get_data = dict(per_page=20, category='all')
    # r = requests.get('http://127.0.0.1:8080/api/v1.0/workflows', headers=headers, params=get_data)
    # result = r.json()
    # print(request.data)
    # data = dict(
    #     username=request.data.get('username'), 
    #     transition_id=request.data.get('transition_id'), 
    #     workflow_id=request.data.get('workflow_id'), 
    #     title=request.data.get('title'), 
    #     suggestion='请协助提供更多信息'
    #     )
    data = request.data

    print(data)
    r = requests.post('http://127.0.0.1:8080/api/v1.0/tickets', headers=headers, json=data)
    result = r.json()
    print(result)
    notify.send(
        request.user,
        recipient=request.user,
        verb='新建了一个工单',
        # target=sn,
        # action_object=result,
        )
    return JsonResponse(result,json_dumps_params={'ensure_ascii':False},safe=False)

@api_view(['get'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated])
def get_tickets(request):
    #获取工单列表
    username = request.user.username
    headers = get_headers(username)
    page = request.GET["page"]
    size = request.GET["size"]

    get_data = dict(per_page=size, page=page,category='all')

    r = requests.get('http://127.0.0.1:8080/api/v1.0/tickets', headers=headers, params=get_data)
    data = r.json()
    print(data)
    result = {
        'count':data['data']['total'],
        'results':data['data']['value']
    }
    print(result)
    return JsonResponse(result,json_dumps_params={'ensure_ascii':False},safe=False)

@api_view(['get'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated])
def get_ticket_detail(request):
    #获取工单详情
    username = request.user.username
    headers = get_headers(username)
    ticket_id = request.GET["id"]
    # ticket_id = 1
    r = requests.get('http://127.0.0.1:8080/api/v1.0/tickets/{}'.format(ticket_id), headers=headers)
    result = r.json()
    print(result)
    return JsonResponse(result,json_dumps_params={'ensure_ascii':False},safe=False)

@api_view(['get'])
def get_ticket_flowstep(request):
    #获取工单流程
    username = request.user.username
    headers = get_headers(username)
    ticket_id = request.GET["id"]
    # ticket_id = 1
    r = requests.get('http://127.0.0.1:8080/api/v1.0/tickets/{}/flowsteps'.format(ticket_id), headers=headers)
    result = r.json()
    print(result)
    return JsonResponse(result,json_dumps_params={'ensure_ascii':False},safe=False)

@api_view(['get'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated])
def get_ticket_flowlogs(request):
    #获取工单操作日志
    username = request.user.username
    headers = get_headers(username)
    ticket_id = request.GET["id"]
    # ticket_id = 1
    r = requests.get('http://127.0.0.1:8080/api/v1.0/tickets/{}/flowlogs'.format(ticket_id), headers=headers)
    result = r.json()
    print(result)
    return JsonResponse(result,json_dumps_params={'ensure_ascii':False},safe=False)

@api_view(['get'])
def get_ticket_transitions(request):
    #获取工单可执行的操作
    username = request.user.username
    headers = get_headers(username)
    ticket_id = request.GET["id"]
    # ticket_id = 1
    r = requests.get('http://127.0.0.1:8080/api/v1.0/tickets/{}/transitions'.format(ticket_id), headers=headers)
    result = r.json()
    print(result)
    return JsonResponse(result,json_dumps_params={'ensure_ascii':False},safe=False)

@api_view(['PATCH'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated])
def handle_ticket(request):
    #新建工单
    username = request.user.username
    ticket_id = request.GET["id"]
    headers = get_headers(username)
    data = request.data
    creator = data["creator"]
    sn = data["sn"]
    suggestion = data["suggestion"]
    print(data)
    r = requests.patch('http://127.0.0.1:8080/api/v1.0/tickets/{}'.format(ticket_id), headers=headers, json=data)
    result = r.json()
    print(result)

    notify.send(
        username,
        recipient=creator,
        verb='处理了您的工单',
        # target=sn,
        action_object=sn,
        )
    return JsonResponse(result,json_dumps_params={'ensure_ascii':False},safe=False)
