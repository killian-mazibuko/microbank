import os, requests
from django.core.management.base import BaseCommand
from core.models import Blacklist

CLIENT_SERVICE_URL = os.getenv('CLIENT_SERVICE_URL', 'http://client-service:8000/api/internal/blacklist-dump/')
INTERNAL_TOKEN = os.getenv('INTERNAL_TOKEN', 'internal-secret-token')

class Command(BaseCommand):
    help = "One-time sync of blacklist from Client Service"

    def handle(self, *args, **kwargs):
        try:
            resp = requests.get(CLIENT_SERVICE_URL, headers={'X-Internal-Token': INTERNAL_TOKEN}, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            ids = set(data.get('blacklisted', []))
            # reset and insert
            Blacklist.objects.all().delete()
            for cid in ids:
                Blacklist.objects.get_or_create(client_id=cid, defaults={'blacklisted': True})
            self.stdout.write(self.style.SUCCESS(f'Synced {len(ids)} blacklisted clients'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to sync blacklist: {e}'))
