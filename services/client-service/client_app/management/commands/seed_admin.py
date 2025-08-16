from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Create default admin user if not exists"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        email = os.environ.get("DEFAULT_ADMIN_EMAIL", "admin@microbank.com")
        password = os.environ.get("DEFAULT_ADMIN_PASSWORD", "admin123")

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password, name="Admin")
            self.stdout.write(self.style.SUCCESS(f"Admin user created: {email}"))
        else:
            self.stdout.write(self.style.WARNING(f"Admin user already exists: {email}"))
