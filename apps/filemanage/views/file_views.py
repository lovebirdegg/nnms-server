# @Time    : 2020/7/24 13:02
# @Author  : liuchao
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from ..serializers.file_serializer import FolderInfoListSerializer,FileInfoSerializer
from common.custom import CommonPagination, RbacPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import FolderInfo,FileInfo
from rest_xops.basic import XopsResponse
from rest_xops.code import *
from django.db.models import Q
from django.db import transaction
from rest_framework.parsers import FileUploadParser
import os

class FolderView(ModelViewSet):
    queryset = FolderInfo.objects.all()
    serializer_class = FolderInfoListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter)
    # pagination_class = CommonPagination
    ordering_fields = ('id',)
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    # def perform_create(self, serializer):
    #     print('perform_create')

    def list(self,request,*args,**kwargs):
        folder_tree = FolderInfo.objects.filter(parent=None,deletedTime=None)
        ser = FolderInfoListSerializer(instance=folder_tree,many=True)  #可允许多个
        return XopsResponse(ser.data)

class FileViewSet(ModelViewSet):
    queryset = FileInfo.objects.all()
    serializer_class = FileInfoSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter)
    pagination_class = CommonPagination
    filter_fields = ('folder',)
    search_fields = ('file_name',)
    ordering_fields = ('id',)
    # parser_classes = (FileUploadParser,)

    # def pre_create(self, obj):
        # print(self.request.FILES['file'].name)

        # obj.samplesheet = self.request.FILES.get('file')
    def perform_create(self, serializer):
        print('perform_create')
        size = self.request.FILES['file'].size
        folder_id = self.request.POST['folder']
        folder = FolderInfo.objects.get(pk=folder_id)
        print(self.request.POST)
        original_filename = self.request.FILES['file'].name
        file_name = original_filename
        filetype = os.path.splitext(self.request.FILES['file'].name)[1].lower()
        if len(filetype) > 0:
            filetype = filetype[1:]

        serializer.save(
            original_filename=original_filename,
            size = size,
            extension = filetype,
            folder = folder,
            file_name=file_name)

    # def create(self, request, *args, **kwargs):
    #     print(self.request.FILES['file'].name)
    #     print(self.request.FILES['file'].size)
    #     print(self.request.FILES['file'])

    #     save_id = transaction.savepoint()
    #     serializer = FileInfoSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     file = serializer.save()
    #     print(file.extension)
    #     transaction.savepoint_commit(save_id)

    #     return Response(status=204)
