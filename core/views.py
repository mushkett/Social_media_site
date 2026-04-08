"""Health check views for monitoring (async-ready)."""

from __future__ import annotations

import time
from typing import Any

from django.core.cache import cache
from django.db import DatabaseError, connection
from django.http import HttpRequest, JsonResponse
from django.views import View

from asgiref.sync import sync_to_async
from redis.exceptions import RedisError


class HealthCheckView(View):
    """
    Async health check endpoint for load balancers and monitoring.

    Returns JSON with status of database and cache connections.
    """

    async def get(self, request: HttpRequest) -> JsonResponse:
        health: dict[str, Any] = {'status': 'healthy', 'timestamp': time.time(), 'checks': {}}

        # Check database (async)
        try:
            await sync_to_async(self._check_db)()
            health['checks']['database'] = {'status': 'ok'}
        except DatabaseError as e:
            health['status'] = 'unhealthy'
            health['checks']['database'] = {'status': 'error', 'message': str(e)}

        # Check cache (Redis) - async
        try:
            cache_ok = await sync_to_async(self._check_cache)()
            if cache_ok:
                health['checks']['cache'] = {'status': 'ok'}
            else:
                health['checks']['cache'] = {'status': 'error', 'message': 'Cache read failed'}
        except (RedisError, ConnectionError) as e:
            # Cache failure is not critical - app can still work
            health['checks']['cache'] = {'status': 'warning', 'message': str(e)}

        status_code = 200 if health['status'] == 'healthy' else 503
        return JsonResponse(health, status=status_code)

    @staticmethod
    def _check_db() -> None:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')

    @staticmethod
    def _check_cache() -> bool:
        cache.set('health_check', 'ok', timeout=10)
        return cache.get('health_check') == 'ok'


class ReadinessCheckView(View):
    """
    Async readiness check for Kubernetes/container orchestration.

    Returns 200 if the app is ready to receive traffic.
    """

    async def get(self, request: HttpRequest) -> JsonResponse:
        # Check if database is accessible
        try:
            await sync_to_async(self._check_db)()
            return JsonResponse({'status': 'ready'}, status=200)
        except DatabaseError as e:
            return JsonResponse({'status': 'not ready', 'error': str(e)}, status=503)

    @staticmethod
    def _check_db() -> None:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')


class LivenessCheckView(View):
    """
    Async liveness check for Kubernetes/container orchestration.

    Returns 200 if the app process is alive.
    """

    async def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'status': 'alive'}, status=200)
