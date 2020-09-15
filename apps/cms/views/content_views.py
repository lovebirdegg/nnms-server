# @Time    : 2020-08-20 15:05:24
# @Author  : code_generator

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes,action

from common.custom import CommonPagination, RbacPermission

from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse,FileResponse,JsonResponse

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_xops.basic import XopsResponse
from rest_xops.code import *
from django.db.models import Q
from django.apps import apps
from ..models import Content


from django.contrib.contenttypes.models import ContentType
from ..serializers.content_serializers import *

class ContentView(ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter)
    pagination_class = CommonPagination
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_fields = ('content_category', 'content_display')
    search_fields = ('content_title', 'content_keyword')

