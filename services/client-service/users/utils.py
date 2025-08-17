import os, jwt, datetime
from django.http import JsonResponse

JWT_SECRET = os.environ.get("JWT_SECRET", "supersecretjwt")

def make_token(user):
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "is_blacklisted": user.is_blacklisted,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12),
        "iat": datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def auth_required(view):
    def wrapper(request, *args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return JsonResponse({"detail":"Auth required"}, status=401)
        token = auth.split(" ",1)[1]
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except Exception as e:
            return JsonResponse({"detail":"Invalid token"}, status=401)
        request.user_payload = data
        return view(request, *args, **kwargs)
    return wrapper
