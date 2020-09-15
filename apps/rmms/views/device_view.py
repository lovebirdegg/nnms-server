# @Time    : 2020/7/24 13:02
# @Author  : liuchao
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from ..serializers.device_serializer import DeviceInfoSerializer, DeviceInfoListSerializer, DeviceListSerializer
from common.custom import CommonPagination, RbacPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models import DeviceInfo
from rest_xops.basic import XopsResponse
from rest_xops.code import *
from django.db.models import Q

from rbac.models import UserProfile

class DeviceListView(ModelViewSet):
    queryset = DeviceInfo.objects.all()
    serializer_class = DeviceInfoListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter)
    pagination_class = CommonPagination
    filter_fields = ('device_type',)
    search_fields = ('hostname',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # authentication_classes = ()
    # permission_classes = ()

    def perform_create(self, serializer):
        createdBy = UserProfile.objects.get(pk=self.request.user.id)
        serializer.save(createdBy=createdBy)
    def perform_update(self, serializer):
        print(self.request.user.id)
        updatedBy = UserProfile.objects.get(pk=self.request.user.id)
        serializer.save(updatedBy=updatedBy)
    def perform_destroy(self, instance):
        instance.updatedBy = UserProfile.objects.get(pk=self.request.user.id)
        instance.delete()