"""
============================================================
RÍO 3 — URLs públicas del sitio
============================================================
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.inicio,           name='inicio'),
    path('servicios/',              views.servicios,        name='servicios'),
    path('proyectos/',              views.proyectos,        name='proyectos'),
    path('proyectos/<int:pk>/',     views.proyecto_detalle, name='proyecto_detalle'),
    path('nosotros/',               views.nosotros,         name='nosotros'),
]
