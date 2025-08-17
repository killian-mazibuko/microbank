from django.http import JsonResponse
from django.urls import resolve
import os

INTERNAL_TOKEN = os.environ.get("INTERNAL_TOKEN", "changeme")

EXEMPT_PATHS = [
    "health",
    "api/schema",
    "api/docs",
]

def InternalTokenMiddleware(get_response):
    def middleware(request):
        path = resolve(request.path_info).route
        if path not in EXEMPT_PATHS:
            token = request.headers.get("X-Internal-Token")
            if token != INTERNAL_TOKEN:
                return JsonResponse({"detail":"Forbidden: missing/invalid internal token"}, status=403)
        return get_response(request)
    return middleware
