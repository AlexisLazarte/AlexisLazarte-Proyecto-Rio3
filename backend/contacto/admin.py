from django.contrib import admin
from .models import MensajeContacto


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'telefono', 'servicio', 'fecha', 'leido']
    list_filter   = ['leido', 'servicio']
    search_fields = ['nombre', 'telefono', 'email']
    list_editable = ['leido']
    readonly_fields = ['fecha']
