# @Time    : 2020/7/24 16:20
# @Author  : liuchao

from rest_framework import serializers
from ..models import FolderInfo,FileInfo
from rest_framework_recursive.fields import RecursiveField


class FolderInfoListSerializer(serializers.ModelSerializer):
    '''
    文件夹序列化
    '''
    # children = serializers.ListField(
    #         read_only=True, source='your_get_children_method', child=RecursiveField()
    #     )
    children = RecursiveField(many=True, required=False)
    class Meta:
        model = FolderInfo
        fields = (
        'id', 'fold_name','parent','children')

class FileInfoSerializer(serializers.ModelSerializer):
    createdBy = serializers.CharField(source='createdBy.name',read_only=True)
    class Meta:
        model = FileInfo
        fields = '__all__'