#!/bin/bash
# ============================================================
# RÍO 3 — Script de configuración del VPS
# Ejecutar UNA SOLA VEZ en el servidor recién creado
#
# Uso:
#   chmod +x setup_vps.sh
#   ./setup_vps.sh
# ============================================================

set -e  # Detener si hay algún error

echo ""
echo "=========================================="
echo "  RÍO 3 — Configuración del VPS"
echo "=========================================="
echo ""

# ==========================================
# 1. ACTUALIZAR EL SISTEMA
# ==========================================
echo "→ Actualizando el sistema..."
apt update && apt upgrade -y

# ==========================================
# 2. INSTALAR DEPENDENCIAS
# ==========================================
echo "→ Instalando Python, Nginx, PostgreSQL..."
apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    postgresql \
    postgresql-contrib \
    git \
    certbot \
    python3-certbot-nginx \
    ufw

# ==========================================
# 3. CONFIGURAR POSTGRESQL
# ==========================================
echo "→ Configurando base de datos..."

# Pedir datos al usuario
read -p "Nombre de la base de datos [rio3_db]: " DB_NAME
DB_NAME=${DB_NAME:-rio3_db}

read -p "Usuario de la base de datos [rio3_user]: " DB_USER
DB_USER=${DB_USER:-rio3_user}

read -s -p "Contraseña para el usuario de BD: " DB_PASSWORD
echo ""

# Crear DB y usuario
sudo -u postgres psql << SQL
CREATE DATABASE ${DB_NAME};
CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';
ALTER ROLE ${DB_USER} SET client_encoding TO 'utf8';
ALTER ROLE ${DB_USER} SET default_transaction_isolation TO 'read committed';
ALTER ROLE ${DB_USER} SET timezone TO 'America/Argentina/Cordoba';
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
SQL

echo "✓ Base de datos configurada"

# ==========================================
# 4. CREAR DIRECTORIO DEL PROYECTO
# ==========================================
echo "→ Creando directorio del proyecto..."
mkdir -p /var/www/rio3
cd /var/www/rio3

# ==========================================
# 5. CLONAR O SUBIR EL PROYECTO
# ==========================================
echo ""
echo "  IMPORTANTE: Subí el proyecto a /var/www/rio3"
echo "  Opciones:"
echo "  a) git clone https://github.com/tuusuario/rio3.git ."
echo "  b) scp -r ./backend usuario@IP:/var/www/rio3/"
echo ""
read -p "¿Ya subiste el proyecto? (s/n): " SUBIDO

if [ "$SUBIDO" != "s" ]; then
    echo "Ejecutá el script de nuevo cuando hayas subido el proyecto."
    exit 1
fi

# ==========================================
# 6. ENTORNO VIRTUAL Y DEPENDENCIAS PYTHON
# ==========================================
echo "→ Creando entorno virtual..."
cd /var/www/rio3
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt

# ==========================================
# 7. ARCHIVO .env
# ==========================================
echo "→ Configurando variables de entorno..."
read -p "Dominio del sitio (ej: rio3.com.ar): " DOMINIO
read -s -p "SECRET_KEY de Django (podés generar una en https://djecrety.ir/): " SECRET_KEY
echo ""
read -p "Email para notificaciones: " EMAIL_USER
read -s -p "App Password de Gmail: " EMAIL_PASS
echo ""
read -p "Email destino para contacto: " EMAIL_DEST

cat > /var/www/rio3/backend/.env << ENV
SECRET_KEY=${SECRET_KEY}
DEBUG=False
ALLOWED_HOSTS=${DOMINIO},www.${DOMINIO},localhost

DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=${EMAIL_USER}
EMAIL_HOST_PASSWORD=${EMAIL_PASS}
EMAIL_DESTINATARIO=${EMAIL_DEST}
ENV

echo "✓ .env creado"

# ==========================================
# 8. MIGRACIONES Y ARCHIVOS ESTÁTICOS
# ==========================================
echo "→ Aplicando migraciones..."
cd /var/www/rio3/backend
source ../venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput

# Crear superusuario admin
echo ""
echo "→ Creando usuario administrador del panel..."
python manage.py createsuperuser

# ==========================================
# 9. CONFIGURAR GUNICORN
# ==========================================
echo "→ Configurando Gunicorn..."
cp /var/www/rio3/deploy/gunicorn.service /etc/systemd/system/rio3.service
systemctl daemon-reload
systemctl enable rio3
systemctl start rio3

# ==========================================
# 10. CONFIGURAR NGINX
# ==========================================
echo "→ Configurando Nginx..."
sed "s/TUDOMINIO/${DOMINIO}/g" /var/www/rio3/deploy/nginx.conf > /etc/nginx/sites-available/rio3
ln -sf /etc/nginx/sites-available/rio3 /etc/nginx/sites-enabled/
nginx -t && systemctl restart nginx

# ==========================================
# 11. FIREWALL
# ==========================================
echo "→ Configurando firewall..."
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

# ==========================================
# 12. SSL CON CERTBOT
# ==========================================
echo "→ Instalando certificado SSL (HTTPS)..."
certbot --nginx -d ${DOMINIO} -d www.${DOMINIO}

echo ""
echo "=========================================="
echo "  ✓ CONFIGURACIÓN COMPLETA"
echo "=========================================="
echo ""
echo "  Sitio público:    https://${DOMINIO}"
echo "  Panel admin:      https://${DOMINIO}/admin-rio3/"
echo "  Admin Django:     https://${DOMINIO}/django-admin/"
echo ""
