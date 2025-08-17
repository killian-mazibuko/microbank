from django.contrib import admin
from django.urls import path
from bank.views import health, balance, deposit, withdraw, transactions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs", SpectacularSwaggerView.as_view(url_name="schema")),
    path("banking/balance", balance),
    path("banking/deposit", deposit),
    path("banking/withdraw", withdraw),
    path("banking/transactions", transactions),
]
