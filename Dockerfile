FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Tizim paketlari
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python paketlari
COPY requirements.txt .
RUN pip install -r requirements.txt

# Loyiha fayllari
COPY . .

# Static fayllarni yig'ish
RUN python manage.py collectstatic --noinput

# Port
EXPOSE 8000

# Boshlash
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py seed_demo && gunicorn navbat_hub.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 2 --log-file -"]
