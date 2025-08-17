from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from django.db import transaction as dbtxn
from decimal import Decimal
from .models import Account, Transaction, Blacklist
from .utils import auth_required

@csrf_exempt
def health(request: HttpRequest):
    return JsonResponse({"status":"ok"})

@csrf_exempt
def _get_or_create_account(user_id):
    acc, _ = Account.objects.get_or_create(user_id=user_id, defaults={"balance": Decimal("0.00")})
    return acc

@csrf_exempt
def _is_blacklisted(user_id):
    try:
        b = Blacklist.objects.get(user_id=user_id)
        return b.is_blacklisted
    except Blacklist.DoesNotExist:
        return False

@auth_required
@csrf_exempt
def balance(request: HttpRequest):
    uid = int(request.user_payload.get("sub"))
    if _is_blacklisted(uid):
        return JsonResponse({"detail":"Blacklisted"}, status=403)
    acc = _get_or_create_account(uid)
    return JsonResponse({"balance": str(acc.balance)})

@csrf_exempt
@auth_required
def deposit(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"detail":"Method not allowed"}, status=405)
    uid = int(request.user_payload.get("sub"))
    if _is_blacklisted(uid):
        return JsonResponse({"detail":"Blacklisted"}, status=403)
    data = json_from_request(request)
    amount = Decimal(str(data.get("amount", "0")))
    if amount <= 0:
        return JsonResponse({"detail":"Amount must be positive"}, status=400)
    acc = _get_or_create_account(uid)
    with dbtxn.atomic():
        acc.balance = acc.balance + amount
        acc.save()
        Transaction.objects.create(account=acc, amount=amount, type="deposit")
    return JsonResponse({"balance": str(acc.balance)})

@csrf_exempt
@auth_required
def withdraw(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"detail":"Method not allowed"}, status=405)
    uid = int(request.user_payload.get("sub"))
    if _is_blacklisted(uid):
        return JsonResponse({"detail":"Blacklisted"}, status=403)
    data = json_from_request(request)
    amount = Decimal(str(data.get("amount", "0")))
    if amount <= 0:
        return JsonResponse({"detail":"Amount must be positive"}, status=400)
    acc = _get_or_create_account(uid)
    with dbtxn.atomic():
        if acc.balance - amount < 0:
            return JsonResponse({"detail":"Insufficient funds"}, status=400)
        acc.balance = acc.balance - amount
        acc.save()
        Transaction.objects.create(account=acc, amount=amount, type="withdraw")
    return JsonResponse({"balance": str(acc.balance)})

@csrf_exempt
@auth_required
def transactions(request: HttpRequest):
    uid = int(request.user_payload.get("sub"))
    if _is_blacklisted(uid):
        return JsonResponse({"detail":"Blacklisted"}, status=403)
    acc = _get_or_create_account(uid)
    data = [{
        "id": t.id, "amount": str(t.amount), "type": t.type, "created_at": t.created_at.isoformat()
    } for t in acc.txns.order_by("-created_at")]
    return JsonResponse({"results": data})

import json
@csrf_exempt
def json_from_request(request):
    try:
        return json.loads(request.body or "{}")
    except Exception:
        return {}
