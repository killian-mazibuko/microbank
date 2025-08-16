import os, json, uuid
from django.db import transaction
from rest_framework import status, generics, permissions, views
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.tokens import AccessToken
from .models import Client
from .serializers import RegisterSerializer, ClientSerializer
from .permissions import IsAdminClient
from .authentication import ClientJWTAuthentication
from .utils import publish_blacklist_event
from django.http import JsonResponse

INTERNAL_TOKEN = os.getenv('INTERNAL_TOKEN', 'internal-token')

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(views.APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            client = Client.objects.get(email=email)
        except Client.DoesNotExist:
            return Response({'detail':'Invalid credentials'}, status=400)
        if not client.check_password(password):
            return Response({'detail':'Invalid credentials'}, status=400)
        token = AccessToken.for_user(client)
        # Use client UUID in 'sub'
        token['sub'] = str(client.id)
        token['email'] = client.email
        token['name'] = client.name
        token['is_admin'] = client.is_admin
        token['is_blacklisted'] = client.is_blacklisted
        return Response({'access': str(token)})

class MeView(views.APIView):
    authentication_classes = [ClientJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(ClientSerializer(request.user).data)

class ClientListView(generics.ListAPIView):
    authentication_classes = [ClientJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminClient]
    serializer_class = ClientSerializer
    queryset = Client.objects.all().order_by('email')

class BlacklistToggleView(views.APIView):
    authentication_classes = [ClientJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminClient]

    def post(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'detail':'Not found'}, status=404)
        client.is_blacklisted = not client.is_blacklisted
        client.save()
        # Publish event
        try:
            publish_blacklist_event(client.id, client.is_blacklisted)
        except Exception as e:
            # Log in real life
            pass
        return Response({'id': str(client.id), 'is_blacklisted': client.is_blacklisted})

@api_view(['GET'])
def health(request):
    return Response({'status':'ok'})

class InternalBlacklistDumpView(views.APIView):
    # Service-to-service endpoint, secured by header token
    def get(self, request):
        token = request.headers.get('X-Internal-Token')
        if token != INTERNAL_TOKEN:
            return Response({'detail': 'Forbidden'}, status=403)
        data = list(Client.objects.filter(is_blacklisted=True).values_list('id', flat=True))
        return Response({'blacklisted': [str(x) for x in data]})
