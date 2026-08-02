from django.urls import path
from . import views

urlpatterns = [
    path('',       views.contacto_enviar, name='contacto_enviar'),
    path('exito/', views.contacto_exito,  name='contacto_exito'),
]
