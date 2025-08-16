from rest_framework.permissions import BasePermission

class IsAdminClient(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and getattr(request.user, 'is_admin', False))
