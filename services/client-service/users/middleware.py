from django.http import JsonResponse
from django.urls import resolve
import os

INTERNAL_TOKEN = os.environ.get("INTERNAL_TOKEN", "supersecretinternal")

EXEMPT_PATHS = [
    "health",
    "api/schema",
    "api/docs",
    "client/register",
    "client/login",
]

def InternalTokenMiddleware(get_response):
    def middleware(request):
        path = resolve(request.path_info).route
        return get_response(request)
    return middleware
