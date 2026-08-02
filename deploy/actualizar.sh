#!/bin/bash
# ============================================================
# RÍO 3 — Script de actualización del sitio
# Ejecutar cada vez que subas cambios al servidor
#
# Uso:
#   chmod +x actualizar.sh
#   ./actualizar.sh
# ============================================================

set -e

echo "→ Activando entorno virtual..."
cd /var/www/rio3
source venv/bin/activate

echo "→ Instalando dependencias nuevas (si las hay)..."
pip install -r backend/requirements.txt

echo "→ Aplicando migraciones..."
cd backend
python manage.py migrate

echo "→ Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "→ Reiniciando Gunicorn..."
systemctl restart rio3

echo ""
echo "✓ Sitio actualizado correctamente"
