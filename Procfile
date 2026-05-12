web: gunicorn navbat_hub.wsgi --log-file -
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
