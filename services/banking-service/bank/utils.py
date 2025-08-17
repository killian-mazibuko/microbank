import os, jwt
from django.http import JsonResponse

JWT_SECRET = os.environ.get("JWT_SECRET", "changeme")

def auth_required(view):
    def wrapper(request, *args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return JsonResponse({"detail":"Auth required"}, status=401)
        token = auth.split(" ",1)[1]
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except Exception:
            return JsonResponse({"detail":"Invalid token"}, status=401)
        request.user_payload = data
        return view(request, *args, **kwargs)
    return wrapper
