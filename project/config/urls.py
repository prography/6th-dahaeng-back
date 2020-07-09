from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('record/', include('record.urls')),
    path('reminder/', include('reminder.urls')),
<<<<<<< HEAD
    path('notice/', include('notice.urls')),
=======
    path('shop/', include('shop.urls')),
>>>>>>> 12166529d74c9a5d75cdf491a4ec961bd8bca39b
    path('api-auth/', include('rest_framework.urls')),
]