# @Time    : {time}
# @Author  : code_generator

from django.urls import path,include
from {app_name}.views import {model_name}_views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'{model_name}s', {model_name}_views.{model_camel_case_name}View, basename="{model_name}s")

urlpatterns = [
    path(r'api/', include(router.urls)),
]