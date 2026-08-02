"""
============================================================
RÍO 3 — URLs del panel de administración
============================================================
"""

from django.urls import path
from . import views_admin

urlpatterns = [
    # Login / Logout
    path('login/',   views_admin.admin_login,  name='admin_login'),
    path('logout/',  views_admin.admin_logout, name='admin_logout'),

    # Dashboard
    path('',         views_admin.admin_dashboard,       name='admin_dashboard'),

    # Proyectos
    path('proyectos/',                views_admin.admin_proyectos_lista,         name='admin_proyectos_lista'),
    path('proyectos/nuevo/',          views_admin.admin_proyecto_nuevo,          name='admin_proyecto_nuevo'),
    path('proyectos/<int:pk>/editar/',   views_admin.admin_proyecto_editar,      name='admin_proyecto_editar'),
    path('proyectos/<int:pk>/eliminar/', views_admin.admin_proyecto_eliminar,    name='admin_proyecto_eliminar'),

    # Fotos
    path('fotos/<int:pk>/eliminar/',  views_admin.admin_foto_eliminar,          name='admin_foto_eliminar'),
]
