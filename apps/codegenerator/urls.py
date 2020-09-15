from django.urls import path,include
from codegenerator import views
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r'folders', file_views.FolderView, basename="folders")
# router.register(r'files', file_views.FileViewSet, basename="files")

# urlpatterns = [
#     path(r'api/get_model_list/', views.get_model_list,name='get_model_list'),
# ]

router = routers.SimpleRouter()
router.register(r'models', views.ContentTypeView, basename="models")
# router.register(r'files', file_views.FileViewSet, basename="files")

urlpatterns = [
    path(r'api/', include(router.urls)),
]