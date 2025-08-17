from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import os

class Command(BaseCommand):
    help = "Create default admin (staff user for admin site)"

    def handle(self, *args, **kwargs):
        email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        password = os.environ.get("ADMIN_PASSWORD", "AdminPass123!")
        username = email.split("@")[0]
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Created admin {email}"))
        else:
            self.stdout.write("Admin exists")
