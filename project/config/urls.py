from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('reminder/', include('reminder.urls')),
    path('api-auth/', include('rest_framework.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
