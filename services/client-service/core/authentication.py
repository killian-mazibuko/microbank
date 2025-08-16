from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Client
from rest_framework import exceptions

class ClientJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        # 'sub' will hold client id per our login implementation
        try:
            client_id = validated_token.get('sub')
            user = Client.objects.get(id=client_id)
            return user
        except Client.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found', code='user_not_found')
