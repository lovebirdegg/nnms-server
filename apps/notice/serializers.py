# @Time    : 2020/8/6 16:20
# @Author  : liuchao

from rest_framework import serializers
from rbac.models import UserProfile
from rbac.serializers.user_serializer import UserInfoListSerializer
class GenericNotificationRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Foo):
            serializer = FooSerializer(value)
        if isinstance(value, Bar):
            serializer = BarSerializer(value)
        return serializer.data


class NotificationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    recipient = UserInfoListSerializer(UserProfile, read_only=True)
    actor = UserInfoListSerializer(UserProfile, read_only=True)
    unread = serializers.BooleanField(read_only=True)
    target = GenericNotificationRelatedField(read_only=True)
    verb = serializers.CharField(read_only=True)
    timestamp = serializers.CharField(read_only=True)