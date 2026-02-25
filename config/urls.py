"""
URL configuration for Camping ACA Lujan project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from apps.landing.media_views import serve_media

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.landing.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('vouchers/', include('apps.vouchers.urls')),
    path('api/', include('apps.analytics.urls')),
    
    # Servir archivos media en producción
    re_path(r'^media/(?P<path>.*)$', serve_media, name='media'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "Camping ACA Luján - Administración"
admin.site.site_title = "Camping ACA Luján"
admin.site.index_title = "Panel de Administración"
