"""
============================================================
RÍO 3 — Vista del formulario de contacto
============================================================
"""

from django.shortcuts   import render, redirect
from django.contrib     import messages
from django.core.mail   import send_mail
from django.conf        import settings

from .forms  import ContactoForm
from .models import MensajeContacto


def contacto_enviar(request):
    """Procesa el formulario de contacto."""

    if request.method == 'POST':
        form = ContactoForm(request.POST)

        if form.is_valid():
            # Guardar en la base de datos
            mensaje = form.save()

            # Enviar email de notificación
            try:
                asunto = f'Nueva consulta de {mensaje.nombre} — Río 3'
                cuerpo = (
                    f'Nombre:   {mensaje.nombre}\n'
                    f'Teléfono: {mensaje.telefono}\n'
                    f'Email:    {mensaje.email or "No indicado"}\n'
                    f'Servicio: {mensaje.get_servicio_display()}\n\n'
                    f'Mensaje:\n{mensaje.mensaje or "Sin mensaje adicional"}\n'
                )
                send_mail(
                    subject      = asunto,
                    message      = cuerpo,
                    from_email   = settings.EMAIL_HOST_USER,
                    recipient_list = [settings.EMAIL_DESTINATARIO],
                    fail_silently = True,
                )
            except Exception:
                # Si el email falla, igual guardamos el mensaje en la DB
                pass

            messages.success(
                request,
                '¡Gracias! Recibimos tu consulta y te contactamos pronto.'
            )
            return redirect('contacto_exito')

        else:
            messages.error(request, 'Revisá los datos del formulario.')

    else:
        form = ContactoForm()

    return render(request, 'contacto/contacto.html', {'form': form})


def contacto_exito(request):
    """Página de confirmación tras enviar el formulario."""
    return render(request, 'contacto/exito.html')
