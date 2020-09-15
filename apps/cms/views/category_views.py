# @Time    : 2020-08-18 10:24:22
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
from ..models import CategoryInfo

from django.contrib.contenttypes.models import ContentType
from ..serializers.category_serializers import *

class CategoryInfoView(ModelViewSet):
    queryset = CategoryInfo.objects.all()
    serializer_class = CategoryInfoSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter)
    pagination_class = CommonPagination
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_fields = ('isActive',)
    search_fields = ('category_name',)

    def list(self,request,*args,**kwargs):
        folder_tree = CategoryInfo.objects.filter(parent=None,deletedTime=None)
        ser = CategoryInfoSerializer(instance=folder_tree,many=True)  #可允许多个
        return XopsResponse(ser.data)

