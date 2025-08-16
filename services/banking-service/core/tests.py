from django.test import TestCase
from rest_framework.test import APIClient
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from .models import Account, Blacklist

class BankingTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.sub = '00000000-0000-0000-0000-000000000000'
        token = AccessToken()
        token['sub'] = self.sub
        token['email'] = 'a@a.com'
        token['name'] = 'A'
        self.client_api.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

    def test_deposit_and_withdraw(self):
        r = self.client_api.post('/api/banking/deposit', {'amount':'10.00'}, format='json')
        self.assertEqual(r.status_code, 200)
        r = self.client_api.post('/api/banking/withdraw', {'amount':'5.00'}, format='json')
        self.assertEqual(r.status_code, 200)
        r = self.client_api.get('/api/banking/balance/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['balance'], '5.00')

    def test_overdraft(self):
        r = self.client_api.post('/api/banking/withdraw', {'amount':'1.00'}, format='json')
        self.assertEqual(r.status_code, 400)

    def test_blacklist_blocks(self):
        Blacklist.objects.create(client_id=self.sub, blacklisted=True)
        r = self.client_api.post('/api/banking/deposit', {'amount':'1.00'}, format='json')
        self.assertEqual(r.status_code, 403)
