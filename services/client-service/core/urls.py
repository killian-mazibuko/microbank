from django.urls import path
from .views import RegisterView, LoginView, MeView, ClientListView, BlacklistToggleView, health, InternalBlacklistDumpView

urlpatterns = [
    path('api/client/health/', health),
    path('api/client/register/', RegisterView.as_view()),
    path('api/client/login/', LoginView.as_view()),
    path('api/client/me/', MeView.as_view()),
    path('api/client/admin/clients/', ClientListView.as_view()),
    path('api/client/admin/clients/<uuid:client_id>/blacklist/', BlacklistToggleView.as_view()),
    path('api/client/api/schema/', lambda r: None),  # placeholder for project urls to mount schema
    path('api/internal/blacklist-dump/', InternalBlacklistDumpView.as_view()),
]
