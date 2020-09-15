from django.urls import path,include
from filemanage.views import file_views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'folders', file_views.FolderView, basename="folders")
router.register(r'files', file_views.FileViewSet, basename="files")

urlpatterns = [
    path(r'api/', include(router.urls)),
]