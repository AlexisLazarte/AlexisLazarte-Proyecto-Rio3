"""
============================================================
RÍO 3 — Registro de modelos en el admin nativo de Django
============================================================
"""

from django.contrib import admin
from .models import Proyecto, Categoria, FotoProyecto


class FotoProyectoInline(admin.TabularInline):
    model  = FotoProyecto
    extra  = 3
    fields = ['foto', 'orden']


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display    = ['titulo', 'categoria', 'estado', 'anio', 'fecha_carga']
    list_filter     = ['estado', 'categoria', 'anio']
    search_fields   = ['titulo', 'descripcion', 'ubicacion']
    list_editable   = ['estado']
    inlines         = [FotoProyectoInline]
    prepopulated_fields = {}


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'orden']
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(FotoProyecto)
class FotoProyectoAdmin(admin.ModelAdmin):
    list_display = ['proyecto', 'orden']
