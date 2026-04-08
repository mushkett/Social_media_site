"""
ASGI config for Social_media project.

Exposes the ASGI callable as a module-level variable named ``application``.
Supports async views with Uvicorn/Daphne.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/

Usage with Uvicorn:
    uvicorn social_media.asgi:application --host 0.0.0.0 --port 8000 --workers 4
"""

from __future__ import annotations

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media.settings.prod')

application = get_asgi_application()
