from django.db import models
import uuid
from django.contrib.auth.hashers import make_password, check_password

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)

    def set_password(self, raw):
        self.password = make_password(raw)

    def check_password(self, raw):
        return check_password(raw, self.password)

    def __str__(self):
        return f"{self.email} ({'admin' if self.is_admin else 'client'})"
