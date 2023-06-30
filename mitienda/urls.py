from django.contrib import admin
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1.0/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path('', include('apps.users.urls')),
    re_path('', include('apps.products.urls')),
    re_path('variations/',include('apps.products.routers')),
    re_path('', include('apps.blog.urls')),
    re_path('', include('apps.orders.urls')),
    re_path('', include('apps.tiendas.urls')),
    re_path('', include('apps.realtime.urls')),
    re_path('', include('apps.services.urls')),
    re_path('', include('apps.estadisticas.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
