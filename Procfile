# ASGI (recommended for async views)
web: python manage.py migrate && uvicorn social_media.asgi:application --host 0.0.0.0 --port ${PORT:-8000} --workers 4

# WSGI fallback (if ASGI is not needed)
# web: python manage.py migrate && gunicorn social_media.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 4
