# @Time    : {time}
# @Author  : code_generator

from rest_framework import serializers
from ..models import {model_name}
from rest_framework_recursive.fields import RecursiveField


class {model_name}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {model_name}
        fields = '__all__'