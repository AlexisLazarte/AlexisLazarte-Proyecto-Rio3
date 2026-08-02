"""
============================================================
RÍO 3 — Formulario de contacto
============================================================
"""

from django import forms
from .models import MensajeContacto


class ContactoForm(forms.ModelForm):

    class Meta:
        model  = MensajeContacto
        fields = ['nombre', 'telefono', 'email', 'servicio', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Tu nombre completo',
                'autocomplete': 'name',
            }),
            'telefono': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Tu número de contacto',
                'autocomplete': 'tel',
            }),
            'email': forms.EmailInput(attrs={
                'class':       'form-control',
                'placeholder': 'tu@correo.com',
                'autocomplete': 'email',
            }),
            'servicio': forms.Select(attrs={
                'class': 'form-select',
            }),
            'mensaje': forms.Textarea(attrs={
                'class':       'form-control',
                'rows':        4,
                'placeholder': 'Tipo de obra, ubicación, superficie aproximada...',
            }),
        }
        labels = {
            'nombre':   'Nombre y apellido',
            'telefono': 'Teléfono',
            'email':    'Email (opcional)',
            'servicio': 'Tipo de servicio',
            'mensaje':  'Contanos tu proyecto',
        }
