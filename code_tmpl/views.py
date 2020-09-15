# @Time    : {time}
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
from ..models import {model_camel_case_name}


from django.contrib.contenttypes.models import ContentType
from ..serializers.{model_name}_serializers import *

class {model_camel_case_name}View(ModelViewSet):
    queryset = {model_camel_case_name}.objects.all()
    serializer_class = {model_camel_case_name}Serializer
    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter)
    pagination_class = CommonPagination
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_fields = ({filter_fields})
    search_fields = ({search_fields})