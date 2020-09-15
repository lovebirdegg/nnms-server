# @Time    : 2020-08-18 10:24:22
# @Author  : code_generator

from rest_framework import serializers
from ..models import CategoryInfo
from rest_framework_recursive.fields import RecursiveField


class CategoryInfoSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, required=False)

    class Meta:
        model = CategoryInfo
        fields = '__all__'