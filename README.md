# Río 3 — Construcción en Seco
### Proyecto Django completo

---

## Estructura del proyecto

```
rio3_django/
├── backend/                  ← código Django
│   ├── rio3/                 ← configuración principal
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── proyectos/            ← app: galería y panel admin
│   │   ├── models.py         ← tablas: Proyecto, Categoria, FotoProyecto
│   │   ├── views.py          ← páginas públicas
│   │   ├── views_admin.py    ← panel de administración
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── urls_admin.py
│   ├── contacto/             ← app: formulario de contacto
│   │   ├── models.py         ← tabla: MensajeContacto
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   ├── templates/            ← HTML (templates Django)
│   │   ├── base/             ← base.html + inicio, servicios, nosotros
│   │   ├── proyectos/        ← galería pública
│   │   ├── contacto/         ← formulario + página de éxito
│   │   └── admin_rio3/       ← panel admin propio
│   ├── static/               ← CSS, JS, imágenes
│   ├── media/                ← fotos subidas por el admin (se crea solo)
│   ├── requirements.txt
│   ├── manage.py
│   └── .env.example          ← copiar como .env y completar
└── deploy/                   ← scripts para el VPS
    ├── setup_vps.sh          ← configuración inicial del servidor
    ├── actualizar.sh         ← actualizar el sitio
    ├── nginx.conf
    └── gunicorn.service
```

---

## PARTE 1 — Correr el proyecto en tu computadora

### Paso 1 — Crear el entorno virtual

```bash
# Ir a la carpeta backend
cd rio3_django/backend

# Crear entorno virtual
python -m venv venv

# Activarlo
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate
```

### Paso 2 — Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3 — Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env
```

Abrí el `.env` y completá los valores. Para desarrollo local podés usar SQLite:

```bash
# Para desarrollo LOCAL más simple, editá settings.py y cambiá la DB a:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

O instalá PostgreSQL localmente y creá la base de datos:

```sql
-- En PostgreSQL:
CREATE DATABASE rio3_db;
CREATE USER rio3_user WITH PASSWORD 'tu-password';
GRANT ALL PRIVILEGES ON DATABASE rio3_db TO rio3_user;
```

### Paso 4 — Crear las tablas y el usuario admin

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Paso 5 — Cargar datos iniciales (categorías)

```bash
python manage.py shell
```

```python
from proyectos.models import Categoria

categorias = [
    {'nombre': 'Steel framing',    'slug': 'steel-framing',    'orden': 1},
    {'nombre': 'Drywall',          'slug': 'drywall',          'orden': 2},
    {'nombre': 'Revestimientos',   'slug': 'revestimientos',   'orden': 3},
    {'nombre': 'EPS Revestimiento','slug': 'eps-revestimiento','orden': 4},
    {'nombre': 'Stands para ferias','slug': 'stands-ferias',   'orden': 5},
]

for cat in categorias:
    Categoria.objects.get_or_create(**cat)

print("Categorías creadas")
exit()
```

### Paso 6 — Correr el servidor de desarrollo

```bash
python manage.py runserver
```

Abrí el navegador en:
- **Sitio público:**   http://127.0.0.1:8000/
- **Panel admin:**     http://127.0.0.1:8000/admin-rio3/
- **Admin Django:**    http://127.0.0.1:8000/django-admin/

---

## PARTE 2 — Subir al VPS de Hostinger

### Paso 1 — Conectarse al VPS por SSH

```bash
ssh root@IP-DE-TU-VPS
```

### Paso 2 — Subir el proyecto al servidor

Desde tu computadora (no desde el servidor):

```bash
# Opción A: con scp
scp -r ./rio3_django/backend root@IP-DEL-VPS:/var/www/rio3/
scp -r ./rio3_django/deploy  root@IP-DEL-VPS:/var/www/rio3/

# Opción B: con Git (recomendado para actualizaciones futuras)
# Primero subí el proyecto a GitHub, luego en el servidor:
# git clone https://github.com/tuusuario/rio3.git /var/www/rio3
```

### Paso 3 — Ejecutar el script de configuración

```bash
# En el servidor VPS:
chmod +x /var/www/rio3/deploy/setup_vps.sh
./var/www/rio3/deploy/setup_vps.sh
```

El script va a:
1. Actualizar el sistema
2. Instalar Python, Nginx y PostgreSQL
3. Crear la base de datos
4. Configurar el entorno virtual
5. Aplicar migraciones
6. Crear el superusuario admin
7. Configurar Gunicorn como servicio
8. Configurar Nginx
9. Instalar certificado SSL (HTTPS) gratis con Certbot

### Paso 4 — Acceder al sitio

- **Sitio público:**   https://tudominio.com/
- **Panel admin:**     https://tudominio.com/admin-rio3/
- **Admin Django:**    https://tudominio.com/django-admin/

---

## PARTE 3 — Actualizar el sitio después del deploy

Cada vez que hagas cambios y los quieras publicar:

```bash
# 1. Subir los archivos modificados al servidor
scp -r ./backend root@IP:/var/www/rio3/

# 2. En el servidor, ejecutar:
./var/www/rio3/deploy/actualizar.sh
```

---

## URLs del proyecto

| URL | Descripción |
|-----|-------------|
| `/` | Inicio |
| `/servicios/` | Servicios |
| `/proyectos/` | Galería de proyectos |
| `/proyectos/?categoria=steel-framing` | Galería filtrada por categoría |
| `/nosotros/` | Nosotros |
| `/contacto/` | Formulario de contacto |
| `/admin-rio3/` | Panel admin propio de Río 3 |
| `/admin-rio3/login/` | Login del panel admin |
| `/admin-rio3/proyectos/` | Lista de proyectos en el admin |
| `/admin-rio3/proyectos/nuevo/` | Crear proyecto |
| `/django-admin/` | Admin nativo de Django |

---

## Comandos útiles en el servidor

```bash
# Ver estado del servicio Django
systemctl status rio3

# Reiniciar Django
systemctl restart rio3

# Ver logs de Django
journalctl -u rio3 -f

# Ver logs de Nginx
tail -f /var/log/nginx/rio3_error.log

# Hacer backup de la base de datos
pg_dump rio3_db > backup_$(date +%Y%m%d).sql
```
