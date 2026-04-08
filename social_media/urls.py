"""Social_media URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from django_ratelimit.decorators import ratelimit

from social_media import views

# Rate-limit admin login to 5 POST attempts per hour per IP
admin.site.login = ratelimit(key='ip', rate='5/h', method='POST', block=True)(admin.site.login)  # type: ignore[method-assign]

urlpatterns = [
    # Health checks (no auth required)
    path('', include('core.urls')),
    # Admin
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    # Main app
    path('', views.HomePage.as_view(), name='home'),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('groups/', include('groups.urls')),
    path('posts/', include('posts.urls')),
]
