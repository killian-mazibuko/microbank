from django.contrib import admin
from django.urls import path
from users.views import register, login_view, me, list_clients, toggle_blacklist, health
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs", SpectacularSwaggerView.as_view(url_name="schema")),
    path("client/register", register),
    path("client/login", login_view),
    path("client/me", me),
    path("client/admin/clients", list_clients),
    path("client/admin/blacklist", toggle_blacklist),
]
