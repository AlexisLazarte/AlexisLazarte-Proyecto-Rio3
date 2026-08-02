"""
============================================================
RÍO 3 — Modelos de la app Proyectos
============================================================
"""

from django.db import models


class Categoria(models.Model):
    """Categorías de proyectos: Steel framing, Drywall, etc."""

    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Slug (URL)',
        help_text='Se genera automáticamente. Ej: steel-framing',
    )
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden de aparición',
    )

    class Meta:
        verbose_name        = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering            = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class Proyecto(models.Model):
    """Proyectos que se muestran en la galería del sitio."""

    ESTADO_BORRADOR   = 'borrador'
    ESTADO_PUBLICADO  = 'publicado'

    ESTADOS = [
        (ESTADO_BORRADOR,  'Borrador'),
        (ESTADO_PUBLICADO, 'Publicado'),
    ]

    # Datos principales
    titulo      = models.CharField(max_length=200, verbose_name='Título')
    categoria   = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='proyectos',
        verbose_name='Categoría',
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción',
        help_text='Descripción breve visible en la galería.',
    )
    ubicacion   = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Ubicación',
        help_text='Ej: Río Tercero, Córdoba',
    )
    anio        = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Año',
    )
    superficie  = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Superficie',
        help_text='Ej: 80 m²',
    )

    # Imagen principal (portada de la galería)
    foto_portada = models.ImageField(
        upload_to='proyectos/',
        verbose_name='Foto de portada',
        help_text='Imagen principal que se muestra en la galería.',
    )

    # Control de publicación
    estado      = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=ESTADO_BORRADOR,
        verbose_name='Estado',
    )
    fecha_carga = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de carga',
    )
    fecha_edicion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última edición',
    )

    class Meta:
        verbose_name        = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering            = ['-fecha_carga']

    def __str__(self):
        return self.titulo

    @property
    def esta_publicado(self):
        return self.estado == self.ESTADO_PUBLICADO


class FotoProyecto(models.Model):
    """Fotos adicionales de un proyecto (además de la portada)."""

    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name='fotos',
        verbose_name='Proyecto',
    )
    foto  = models.ImageField(
        upload_to='proyectos/galeria/',
        verbose_name='Foto',
    )
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden',
    )

    class Meta:
        verbose_name        = 'Foto de proyecto'
        verbose_name_plural = 'Fotos de proyecto'
        ordering            = ['orden']

    def __str__(self):
        return f'Foto de {self.proyecto.titulo}'
