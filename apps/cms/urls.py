# @Time    : 2020-08-18 10:24:22
# @Author  : code_generator

from django.urls import path,include
from cms.views import category_views,content_views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'categoryinfos', category_views.CategoryInfoView, basename="categoryinfos")
router.register(r'contents', content_views.ContentView, basename="contents")

urlpatterns = [
    path(r'api/', include(router.urls)),
]