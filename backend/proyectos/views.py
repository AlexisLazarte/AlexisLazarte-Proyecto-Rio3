"""
============================================================
RÍO 3 — Vistas públicas del sitio
============================================================
"""

from django.shortcuts import render, get_object_or_404
from .models import Proyecto, Categoria


def inicio(request):
    """Renderiza la página de inicio."""
    return render(request, 'base/inicio.html')


def servicios(request):
    """Renderiza la página de servicios."""
    return render(request, 'base/servicios.html')


def proyectos(request):
    """Galería de proyectos publicados, con filtro por categoría."""

    categoria_slug   = request.GET.get('categoria', None)
    categorias       = Categoria.objects.all()
    proyectos_qs     = Proyecto.objects.filter(
        estado=Proyecto.ESTADO_PUBLICADO
    ).select_related('categoria')

    categoria_activa = None
    if categoria_slug:
        try:
            categoria_activa = Categoria.objects.get(slug=categoria_slug)
            proyectos_qs     = proyectos_qs.filter(categoria=categoria_activa)
        except Categoria.DoesNotExist:
            pass

    context = {
        'proyectos':        proyectos_qs,
        'categorias':       categorias,
        'categoria_activa': categoria_activa,
    }
    return render(request, 'proyectos/galeria.html', context)


def proyecto_detalle(request, pk):
    """Detalle de un proyecto con todas sus fotos."""
    proyecto = get_object_or_404(
        Proyecto,
        pk=pk,
        estado=Proyecto.ESTADO_PUBLICADO
    )
    fotos = proyecto.fotos.all().order_by('orden')
    return render(request, 'proyectos/detalle.html', {
        'proyecto': proyecto,
        'fotos':    fotos,
    })


def nosotros(request):
    """Renderiza la página de nosotros."""
    return render(request, 'base/nosotros.html')
