import os
from django.core.management.base import BaseCommand
from core.models import Client

class Command(BaseCommand):
    help = "Create a demo admin if env says so"

    def handle(self, *args, **kwargs):
        if os.getenv('CREATE_DEMO_ADMIN','0') != '1':
            self.stdout.write(self.style.WARNING('Skipping demo admin creation'))
            return
        email = os.getenv('DEMO_ADMIN_EMAIL','admin@example.com')
        password = os.getenv('DEMO_ADMIN_PASSWORD','adminpass')
        name = 'Admin'
        obj, created = Client.objects.get_or_create(email=email, defaults={'name': name, 'is_admin': True})
        if created or not obj.check_password(password):
            obj.set_password(password)
            obj.is_admin = True
            obj.save()
        self.stdout.write(self.style.SUCCESS(f'Ensured demo admin {email}'))
