import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Crea un superusuario automático para la demo en Render'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'admin@rio3.com')
        password = os.getenv('ADMIN_PASSWORD', 'Rio3Demo2026!')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superusuario "{username}" creado con éxito.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'El usuario "{username}" ya existe.'))