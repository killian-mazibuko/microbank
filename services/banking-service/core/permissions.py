from rest_framework.permissions import BasePermission
from .models import Blacklist

class NotBlacklisted(BasePermission):
    def has_permission(self, request, view):
        client_id = getattr(request.user, 'id', None)
        if not client_id:
            return False
        return not Blacklist.objects.filter(client_id=client_id, blacklisted=True).exists()
