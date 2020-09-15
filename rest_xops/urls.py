from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
import notifications.urls

urlpatterns = [
    path(r'', include('rbac.urls')),
    path(r'', include('cmdb.urls')),
    path(r'', include('rmms.urls')),
    path(r'', include('workflow.urls')),
    path(r'', include('notice.urls')),
    path(r'', include('deployment.urls')),
    path(r'', include('filemanage.urls')),
    path(r'', include('codegenerator.urls')),
    path(r'', include('cms.urls')),
    path('docs/', include_docs_urls()),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
