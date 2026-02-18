import json
import pika

from foodgram.rabbitmq import get_rabbitmq_connection


def publish_task(api_name, recipe_id, **extra_params):
    print(f" [x] {api_name}")
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    channel.exchange_declare(
        exchange='foodgram_tasks',
        exchange_type='direct',
        durable=True
    )

    message = {
        'api': api_name,
        'recipe_id': recipe_id,
        **extra_params
    }

    channel.basic_publish(
        exchange='foodgram_tasks',
        routing_key=api_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    connection.close()
