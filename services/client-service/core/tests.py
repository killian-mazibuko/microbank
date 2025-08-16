from django.test import TestCase
from rest_framework.test import APIClient
from .models import Client

class ClientTests(TestCase):
    def setUp(self):
        self.api = APIClient()

    def test_register_and_login(self):
        r = self.api.post('/api/client/register/', {'email':'u@e.com', 'name':'User', 'password':'secret123'}, format='json')
        self.assertEqual(r.status_code, 201)
        r = self.api.post('/api/client/login/', {'email':'u@e.com','password':'secret123'}, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertIn('access', r.data)
