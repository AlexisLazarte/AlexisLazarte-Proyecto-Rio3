"""
============================================================
RÍO 3 — Modelo de la app Contacto
============================================================
"""

from django.db import models


class MensajeContacto(models.Model):
    """Guarda cada consulta enviada desde el formulario de contacto."""

    SERVICIOS = [
        ('steel',          'Steel framing'),
        ('drywall',        'Drywall / cielorrasos'),
        ('revestimientos', 'Revestimientos'),
        ('eps',            'EPS Revestimiento'),
        ('stands',         'Stands para ferias'),
        ('otro',           'Otro / no estoy seguro'),
    ]

    nombre   = models.CharField(max_length=200, verbose_name='Nombre')
    telefono = models.CharField(max_length=50,  verbose_name='Teléfono')
    email    = models.EmailField(blank=True,     verbose_name='Email')
    servicio = models.CharField(
        max_length=50,
        choices=SERVICIOS,
        blank=True,
        verbose_name='Servicio consultado',
    )
    mensaje  = models.TextField(blank=True, verbose_name='Mensaje')

    fecha    = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    leido    = models.BooleanField(default=False, verbose_name='Leído')

    class Meta:
        verbose_name        = 'Mensaje de contacto'
        verbose_name_plural = 'Mensajes de contacto'
        ordering            = ['-fecha']

    def __str__(self):
        return f'{self.nombre} — {self.fecha.strftime("%d/%m/%Y %H:%M")}'
