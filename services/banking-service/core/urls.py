from django.urls import path
from .views import DepositView, WithdrawView, BalanceView, health

urlpatterns = [
    path('api/banking/health/', health),
    path('api/banking/balance/', BalanceView.as_view()),
    path('api/banking/deposit', DepositView.as_view()),
    path('api/banking/withdraw', WithdrawView.as_view()),
]
