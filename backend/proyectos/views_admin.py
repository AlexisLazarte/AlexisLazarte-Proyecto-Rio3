"""
============================================================
RÍO 3 — Vistas del panel de administración propio
Protegidas con @login_required
============================================================
"""

from django.shortcuts        import render, redirect, get_object_or_404
from django.contrib.auth     import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib          import messages
from .models  import Proyecto, Categoria, FotoProyecto
from .forms   import ProyectoForm


# ============================================================
# LOGIN / LOGOUT
# ============================================================

def admin_login(request):
    """Login del panel admin de Río 3."""

    # Si ya está logueado, redirigir al panel
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user     = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'admin_rio3/login.html')


def admin_logout(request):
    """Logout del panel admin."""
    logout(request)
    return redirect('inicio')


# ============================================================
# DASHBOARD
# ============================================================

@login_required
def admin_dashboard(request):
    """Panel principal con métricas."""

    metricas = {
        'total':      Proyecto.objects.count(),
        'publicados': Proyecto.objects.filter(estado=Proyecto.ESTADO_PUBLICADO).count(),
        'borradores': Proyecto.objects.filter(estado=Proyecto.ESTADO_BORRADOR).count(),
        'fotos':      FotoProyecto.objects.count(),
    }

    proyectos_recientes = Proyecto.objects.select_related('categoria').order_by('-fecha_carga')[:10]

    context = {
        'metricas':            metricas,
        'proyectos_recientes': proyectos_recientes,
    }
    return render(request, 'admin_rio3/dashboard.html', context)


# ============================================================
# CRUD DE PROYECTOS
# ============================================================

@login_required
def admin_proyectos_lista(request):
    """Lista de todos los proyectos."""
    proyectos = Proyecto.objects.select_related('categoria').order_by('-fecha_carga')
    return render(request, 'admin_rio3/proyectos_lista.html', {'proyectos': proyectos})


@login_required
def admin_proyecto_nuevo(request):
    """Crear un nuevo proyecto."""

    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save()

            # Procesar fotos adicionales
            fotos = request.FILES.getlist('fotos_adicionales')
            for i, foto in enumerate(fotos):
                FotoProyecto.objects.create(
                    proyecto=proyecto,
                    foto=foto,
                    orden=i,
                )

            messages.success(request, f'Proyecto "{proyecto.titulo}" creado correctamente.')
            return redirect('admin_proyectos_lista')
        else:
            messages.error(request, 'Revisá los datos del formulario.')
    else:
        form = ProyectoForm()

    return render(request, 'admin_rio3/proyecto_form.html', {
        'form':   form,
        'titulo': 'Nuevo proyecto',
        'accion': 'Publicar proyecto',
    })


@login_required
def admin_proyecto_editar(request, pk):
    """Editar un proyecto existente."""

    proyecto = get_object_or_404(Proyecto, pk=pk)

    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES, instance=proyecto)
        if form.is_valid():
            form.save()

            # Agregar fotos adicionales si se subieron
            fotos = request.FILES.getlist('fotos_adicionales')
            ultimo_orden = proyecto.fotos.count()
            for i, foto in enumerate(fotos):
                FotoProyecto.objects.create(
                    proyecto=proyecto,
                    foto=foto,
                    orden=ultimo_orden + i,
                )

            messages.success(request, f'Proyecto "{proyecto.titulo}" actualizado.')
            return redirect('admin_proyectos_lista')
        else:
            messages.error(request, 'Revisá los datos del formulario.')
    else:
        form = ProyectoForm(instance=proyecto)

    return render(request, 'admin_rio3/proyecto_form.html', {
        'form':     form,
        'proyecto': proyecto,
        'titulo':   f'Editar: {proyecto.titulo}',
        'accion':   'Guardar cambios',
    })


@login_required
def admin_proyecto_eliminar(request, pk):
    """Eliminar un proyecto."""

    proyecto = get_object_or_404(Proyecto, pk=pk)

    if request.method == 'POST':
        titulo = proyecto.titulo
        proyecto.delete()
        messages.success(request, f'Proyecto "{titulo}" eliminado.')
        return redirect('admin_proyectos_lista')

    return render(request, 'admin_rio3/proyecto_confirmar_eliminar.html', {
        'proyecto': proyecto,
    })


@login_required
def admin_foto_eliminar(request, pk):
    """Eliminar una foto adicional de un proyecto."""

    foto = get_object_or_404(FotoProyecto, pk=pk)
    proyecto_pk = foto.proyecto.pk

    if request.method == 'POST':
        foto.delete()
        messages.success(request, 'Foto eliminada.')

    return redirect('admin_proyecto_editar', pk=proyecto_pk)
