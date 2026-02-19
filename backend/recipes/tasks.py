# import json
# import pika
#
# from foodgram.rabbitmq import get_rabbitmq_connection
#
#
# def publish_task(api_name, recipe_id, **extra_params):
#     print(f" [x] {api_name}")
#     connection = get_rabbitmq_connection()
#     channel = connection.channel()
#
#     channel.exchange_declare(
#         exchange='foodgram_tasks',
#         exchange_type='direct',
#         durable=True
#     )
#
#     message = {
#         'api': api_name,
#         'recipe_id': recipe_id,
#         **extra_params
#     }
#
#     channel.basic_publish(
#         exchange='foodgram_tasks',
#         routing_key=api_name,
#         body=json.dumps(message),
#         properties=pika.BasicProperties(
#             delivery_mode=2,
#         )
#     )
#     connection.close()


import time
import requests
import json
import os

from celery import shared_task


@shared_task(bind=True, max_retries=3)
def fetch_foodish_image(self, recipe_id):
    try:
        response = requests.get('https://foodish-api.com/api/', timeout=10)
        response.raise_for_status()
        data = response.json()

        output_dir = os.environ.get('FOODISH_OUTPUT_DIR', '/output/foodish')
        os.makedirs(output_dir, exist_ok=True)

        filename = f"foodish_{recipe_id}_{int(time.time())}.json"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        return f"Saved to {filepath}"

    except Exception as exc:
        # Автоматический повтор при ошибке
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def fetch_nyt_article(self, recipe_id):
    api_key = os.environ.get('NYT_API_KEY')
    if not api_key:
        raise ValueError("NYT_API_KEY not set")

    try:
        url = f"https://api.nytimes.com/svc/mostpopular/v2/shared/1/facebook.json?api-key={api_key}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        output_dir = os.environ.get('NYT_OUTPUT_DIR', '/output/nyt')
        os.makedirs(output_dir, exist_ok=True)

        filename = f"nyt_{recipe_id}_{int(time.time())}.json"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        return f"Saved to {filepath}"

    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)