from django.db import models

class Account(models.Model):
    user_id = models.IntegerField(unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="txns")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=20)  # deposit/withdraw
    created_at = models.DateTimeField(auto_now_add=True)

class Blacklist(models.Model):
    user_id = models.IntegerField(unique=True)
    is_blacklisted = models.BooleanField(default=False)
