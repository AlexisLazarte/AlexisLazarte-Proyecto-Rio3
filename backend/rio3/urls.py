"""
============================================================
RÍO 3 — URLs principales
============================================================
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Admin Django nativo (para emergencias)
    path('django-admin/', admin.site.urls),

    # Sitio público
    path('',              include('proyectos.urls')),
    path('contacto/',     include('contacto.urls')),

    # Panel admin propio de Río 3
    path('admin-rio3/',   include('proyectos.urls_admin')),

]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
