import pika

from django.conf import settings


def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(
        settings.RABBITMQ_USER,
        settings.RABBITMQ_PASSWORD
    )

    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        virtual_host='foodgram',
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300
    )

    return pika.BlockingConnection(parameters)

