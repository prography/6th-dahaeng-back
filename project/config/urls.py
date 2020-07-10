from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('record/', include('record.urls')),
    path('reminder/', include('reminder.urls')),
    path('notice/', include('notice.urls')),
    path('shop/', include('shop.urls')),
    path('api-auth/', include('rest_framework.urls')),
]