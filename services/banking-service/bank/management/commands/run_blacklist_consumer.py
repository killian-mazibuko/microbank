from django.core.management.base import BaseCommand
from bank.models import Blacklist
import os, json, pika

class Command(BaseCommand):
    help = "Run RabbitMQ consumer to sync blacklist"

    def handle(self, *args, **kwargs):
        host = os.environ.get("RABBITMQ_HOST", "rabbitmq")
        user = os.environ.get("RABBITMQ_USER", "guest")
        pw = os.environ.get("RABBITMQ_PASS", "guest")
        vhost = os.environ.get("RABBITMQ_VHOST", "/")
        credentials = pika.PlainCredentials(user, pw)
        params = pika.ConnectionParameters(host=host, virtual_host=vhost, credentials=credentials, heartbeat=60)
        try:
            conn = pika.BlockingConnection(params)
        except Exception as e:
            self.stderr.write(f"RabbitMQ connection failed: {e}")
            return
        ch = conn.channel()
        ch.exchange_declare(exchange="blacklist", exchange_type="fanout", durable=True)
        q = ch.queue_declare(queue="", exclusive=True)
        ch.queue_bind(exchange="blacklist", queue=q.method.queue)

        self.stdout.write("Blacklist consumer running...")
        for method, properties, body in ch.consume(q.method.queue, inactivity_timeout=None):
            if body is None:
                continue
            try:
                msg = json.loads(body.decode("utf-8"))
                uid = int(msg["user_id"])
                is_b = bool(msg["is_blacklisted"])
                obj, _ = Blacklist.objects.get_or_create(user_id=uid, defaults={"is_blacklisted": is_b})
                obj.is_blacklisted = is_b
                obj.save()
                ch.basic_ack(method.delivery_tag)
            except Exception as e:
                self.stderr.write(f"Error processing message: {e}")
                ch.basic_nack(method.delivery_tag, requeue=False)
