from rest_framework import views, status, permissions, throttling
from rest_framework.response import Response
from django.db import transaction
from decimal import Decimal
from .models import Account, Transaction, Blacklist
from .serializers import AmountSerializer, BalanceResponseSerializer, TransactionSerializer
from .authentication import ClientJWTAuthentication
from .permissions import NotBlacklisted
from django.utils import timezone

class DepositThrottle(throttling.ScopedRateThrottle):
    scope = 'banking.deposit'

class WithdrawThrottle(throttling.ScopedRateThrottle):
    scope = 'banking.withdraw'

class BalanceView(views.APIView):
    authentication_classes = [ClientJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, NotBlacklisted]

    def get(self, request):
        client_id = request.user.id
        acct, _ = Account.objects.get_or_create(client_id=client_id)
        txns = acct.transactions.order_by('-created_at')[:50]
        data = {'balance': acct.balance, 'transactions': TransactionSerializer(txns, many=True).data}
        return Response(data)

class DepositView(views.APIView):
    authentication_classes = [ClientJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, NotBlacklisted]
    throttle_classes = [DepositThrottle]

    def post(self, request):
        ser = AmountSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        amt = ser.validated_data['amount']
        client_id = request.user.id
        with transaction.atomic():
            acct, _ = Account.objects.select_for_update().get_or_create(client_id=client_id)
            acct.balance = (acct.balance or Decimal('0')) + amt
            acct.save()
            Transaction.objects.create(account=acct, type='deposit', amount=amt)
        return Response({'balance': str(acct.balance)})

class WithdrawView(views.APIView):
    authentication_classes = [ClientJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, NotBlacklisted]
    throttle_classes = [WithdrawThrottle]

    def post(self, request):
        ser = AmountSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        amt = ser.validated_data['amount']
        client_id = request.user.id
        with transaction.atomic():
            acct, _ = Account.objects.select_for_update().get_or_create(client_id=client_id)
            if acct.balance < amt:
                return Response({'detail':'Insufficient funds'}, status=400)
            acct.balance -= amt
            acct.save()
            Transaction.objects.create(account=acct, type='withdraw', amount=amt)
        return Response({'balance': str(acct.balance)})

from rest_framework.decorators import api_view
@api_view(['GET'])
def health(request):
    return Response({'status':'ok'})
