# @Time    : 2020-08-20 15:05:24
# @Author  : code_generator

from django.urls import path,include
from cms.views import content_views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'contents', content_views.ContentView, basename="contents")

urlpatterns = [
    path(r'api/', include(router.urls)),
]