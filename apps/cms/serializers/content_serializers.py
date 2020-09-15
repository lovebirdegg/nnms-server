# @Time    : 2020-08-20 15:05:24
# @Author  : code_generator

from rest_framework import serializers
from ..models import Content
from rest_framework_recursive.fields import RecursiveField


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'