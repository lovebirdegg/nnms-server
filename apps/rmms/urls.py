from django.urls import path,include
from rmms.views import device_view
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'devices', device_view.DeviceListView, basename="devices")

urlpatterns = [
    path(r'api/', include(router.urls)),
]