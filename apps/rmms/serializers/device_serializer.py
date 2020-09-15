# @Time    : 2020/7/24 16:20
# @Author  : liuchao

from rest_framework import serializers
from ..models import DeviceInfo


class DeviceInfoSerializer(serializers.ModelSerializer):
    '''
    设备信息序列化
    '''

    class Meta:
        model = DeviceInfo
        fields = '__all__'


class DeviceInfoListSerializer(serializers.ModelSerializer):
    '''
    设备列表序列化
    '''

    class Meta:
        model = DeviceInfo
        fields = (
        'id', 'code','hostname', 'device_type', 'desc','longitude','latitude','buy_date')
        depth = 1


class DeviceListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    ip = serializers.CharField(source='hostname')
    # code = serializers.CharField(source='code')
