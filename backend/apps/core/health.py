from django.core.cache import cache
from django.db import connection
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class LiveHealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


class ReadyHealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        checks = {"database": False, "cache": False}
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            checks["database"] = True
        except Exception:
            pass
        try:
            cache.set("healthcheck", "ok", timeout=5)
            checks["cache"] = cache.get("healthcheck") == "ok"
        except Exception:
            pass
        ready = all(checks.values())
        return Response({"status": "ok" if ready else "not_ready", "checks": checks}, status=200 if ready else 503)
