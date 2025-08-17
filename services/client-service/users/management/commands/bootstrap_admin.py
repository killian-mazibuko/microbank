from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Create default admin from env"

    def handle(self, *args, **kwargs):
        email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        password = os.environ.get("ADMIN_PASSWORD", "AdminPass123!")
        username = email.split("@")[0]
        user, created = User.objects.get_or_create(username=username, defaults={
            "email": email, "is_staff": True, "is_superuser": True
        })
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created admin {email}"))
        else:
            self.stdout.write("Admin exists")
