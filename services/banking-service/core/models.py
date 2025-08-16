from django.db import models
import uuid
from decimal import Decimal

class Account(models.Model):
    client_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

class Transaction(models.Model):
    TYPE_CHOICES = (('deposit','deposit'), ('withdraw','withdraw'))
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Blacklist(models.Model):
    client_id = models.UUIDField(primary_key=True, editable=True)
    blacklisted = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
