"""Core app URL configuration."""

from django.urls import path

from health_check.views import HealthCheckView as DjangoHealthCheckView

from core.views import HealthCheckView, LivenessCheckView, ReadinessCheckView

app_name = 'core'

urlpatterns = [
    # Custom health checks (lightweight, async)
    path('health/', HealthCheckView.as_view(), name='health'),
    path('ready/', ReadinessCheckView.as_view(), name='ready'),
    path('live/', LivenessCheckView.as_view(), name='live'),
    # django-health-check (comprehensive, with HTML/JSON output)
    path('ht/', DjangoHealthCheckView.as_view(), name='health_check'),
]
