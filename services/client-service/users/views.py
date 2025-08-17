import json, os, pika
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from .serializers import RegisterSerializer, UserSerializer
from .utils import make_token, auth_required

User = get_user_model()

@csrf_exempt
def health(request: HttpRequest):
    return JsonResponse({"status":"ok"})

@csrf_exempt
def register(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"detail":"Method not allowed"}, status=405)
    data = json.loads(request.body or "{}")
    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        return JsonResponse(UserSerializer(user).data, status=201)
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def login_view(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"detail":"Method not allowed"}, status=405)
    data = json.loads(request.body or "{}")
    username = data.get("username")
    password = data.get("password")
    user = authenticate(username=username, password=password)
    if not user:
        return JsonResponse({"detail":"Invalid credentials"}, status=400)
    token = make_token(user)
    return JsonResponse({"token": token})

@csrf_exempt
@auth_required
def me(request: HttpRequest):
    uid = request.user_payload.get("sub")
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return JsonResponse({"detail":"Not found"}, status=404)
    return JsonResponse(UserSerializer(user).data)

# Admin endpoints
@csrf_exempt
@auth_required
def list_clients(request: HttpRequest):
    # Require staff
    uid = request.user_payload.get("sub")
    user = User.objects.get(id=uid)
    if not user.is_staff:
        return JsonResponse({"detail":"Forbidden"}, status=403)
    data = [UserSerializer(u).data for u in User.objects.all().order_by("id")]
    return JsonResponse({"results": data})

@auth_required
@csrf_exempt
def toggle_blacklist(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"detail":"Method not allowed"}, status=405)
    uid = request.user_payload.get("sub")
    admin = User.objects.get(id=uid)
    if not admin.is_staff:
        return JsonResponse({"detail":"Forbidden"}, status=403)
    body = json.loads(request.body or "{}")
    target_id = body.get("user_id")
    is_blacklisted = body.get("is_blacklisted")
    try:
        target = User.objects.get(id=target_id)
    except User.DoesNotExist:
        return JsonResponse({"detail":"User not found"}, status=404)
    target.is_blacklisted = bool(is_blacklisted)
    target.save()

    # Publish to RabbitMQ for async propagation
    host = os.environ.get("RABBITMQ_HOST", "rabbitmq")
    user = os.environ.get("RABBITMQ_USER", "guest")
    pw = os.environ.get("RABBITMQ_PASS", "guest")
    vhost = os.environ.get("RABBITMQ_VHOST", "/")
    credentials = pika.PlainCredentials(user, pw)
    params = pika.ConnectionParameters(host=host, virtual_host=vhost, credentials=credentials)
    try:
        conn = pika.BlockingConnection(params)
        ch = conn.channel()
        ch.exchange_declare(exchange="blacklist", exchange_type="fanout", durable=True)
        msg = json.dumps({"user_id": target.id, "is_blacklisted": target.is_blacklisted})
        ch.basic_publish(exchange="blacklist", routing_key="", body=msg.encode("utf-8"))
        conn.close()
    except Exception as e:
        # Log only; async best-effort
        pass

    return JsonResponse({"ok": True, "user": UserSerializer(target).data})
