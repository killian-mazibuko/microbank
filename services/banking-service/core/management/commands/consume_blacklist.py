import os, json, pika
from django.core.management.base import BaseCommand
from core.models import Blacklist

RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')
BLACKLIST_EXCHANGE = os.getenv('BLACKLIST_EXCHANGE', 'blacklist_events')

class Command(BaseCommand):
    help = "Subscribe to blacklist events and update local blacklist table"

    def handle(self, *args, **kwargs):
        params = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.exchange_declare(exchange=BLACKLIST_EXCHANGE, exchange_type='fanout', durable=True)
        queue = channel.queue_declare(queue='', exclusive=True).method.queue
        channel.queue_bind(exchange=BLACKLIST_EXCHANGE, queue=queue)

        self.stdout.write(self.style.SUCCESS('Listening for blacklist events...'))
        def callback(ch, method, properties, body):
            data = json.loads(body.decode('utf-8'))
            client_id = data.get('client_id')
            is_blacklisted = data.get('is_blacklisted', True)
            if is_blacklisted:
                Blacklist.objects.update_or_create(client_id=client_id, defaults={'blacklisted': True})
            else:
                Blacklist.objects.filter(client_id=client_id).delete()
            self.stdout.write(f'Updated blacklist for {client_id}: {is_blacklisted}')

        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            connection.close()
