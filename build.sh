#!/usr/bin/env bash
# Render uchun build skripti
set -o errexit

echo "📦 Paketlar o'rnatilmoqda..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🎨 Static fayllar yig'ilmoqda..."
python manage.py collectstatic --noinput --clear

echo "🗄  Migratsiyalar bajarilmoqda..."
python manage.py migrate --noinput

echo "🌱 Demo ma'lumotlar yuklanmoqda..."
python manage.py seed_demo

echo "✅ Build tugadi!"
