import os, json, pika

RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')
BLACKLIST_EXCHANGE = os.getenv('BLACKLIST_EXCHANGE', 'blacklist_events')

def publish_blacklist_event(client_id, is_blacklisted):
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=BLACKLIST_EXCHANGE, exchange_type='fanout', durable=True)
    payload = json.dumps({'client_id': str(client_id), 'is_blacklisted': bool(is_blacklisted)})
    channel.basic_publish(exchange=BLACKLIST_EXCHANGE, routing_key='', body=payload)
    connection.close()
