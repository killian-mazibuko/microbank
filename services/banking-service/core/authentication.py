from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

class ClientJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        # We don't have a User model here; return a simple object-like with attributes
        class _User:
            def __init__(self, client_id, email, name, is_admin=False):
                self.id = client_id
                self.email = email
                self.name = name
                self.is_admin = is_admin
        sub = validated_token.get('sub')
        if not sub:
            raise exceptions.AuthenticationFailed('Invalid token: missing sub')
        return _User(sub, validated_token.get('email'), validated_token.get('name'), validated_token.get('is_admin', False))
