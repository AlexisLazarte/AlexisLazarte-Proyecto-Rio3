"""
============================================================
RÍO 3 — Formularios de la app Proyectos
============================================================
"""

from django import forms
from .models import Proyecto


class ProyectoForm(forms.ModelForm):
    """Formulario para crear y editar proyectos desde el panel admin."""

    class Meta:
        model   = Proyecto
        fields  = [
            'titulo',
            'categoria',
            'descripcion',
            'ubicacion',
            'anio',
            'superficie',
            'foto_portada',
            'estado',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Ej: Vivienda Barrio Norte',
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
            }),
            'descripcion': forms.Textarea(attrs={
                'class':       'form-control',
                'rows':        3,
                'placeholder': 'Describí brevemente la obra...',
            }),
            'ubicacion': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Ej: Río Tercero, Córdoba',
            }),
            'anio': forms.NumberInput(attrs={
                'class':       'form-control',
                'placeholder': '2025',
                'min':         2000,
                'max':         2099,
            }),
            'superficie': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Ej: 80 m²',
            }),
            'foto_portada': forms.FileInput(attrs={
                'class':  'form-control',
                'accept': 'image/*',
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'titulo':       'Título del proyecto',
            'categoria':    'Categoría',
            'descripcion':  'Descripción breve',
            'ubicacion':    'Ubicación',
            'anio':         'Año',
            'superficie':   'Superficie (opcional)',
            'foto_portada': 'Foto de portada',
            'estado':       'Estado',
        }
