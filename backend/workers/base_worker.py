# import os
# import argparse
# import pika
#
# from pathlib import Path
#
# def parse_args():
#     parser = argparse.ArgumentParser(description='RabbitMQ Worker')
#     parser.add_argument('--queue', required=True, help='Queue name to consume')
#     parser.add_argument('--output-dir', default='/output', help='Directory to save JSON files')
#     return parser.parse_args()
#
#
# def get_rabbitmq_connection():
#     credentials = pika.PlainCredentials(
#         os.environ['RABBITMQ_USER'],
#         os.environ['RABBITMQ_PASSWORD']
#     )
#     parameters = pika.ConnectionParameters(
#         host=os.environ['RABBITMQ_HOST'],
#         port=int(os.environ.get('RABBITMQ_PORT', 5672)),
#         virtual_host='foodgram',
#         credentials=credentials,
#         heartbeat=600
#     )
#     return pika.BlockingConnection(parameters)
#
#
# def run_worker(callback):
#     args = parse_args()
#     queue_name = args.queue
#     output_dir = Path(args.output_dir)
#     output_dir.mkdir(parents=True, exist_ok=True)
#
#     connection = get_rabbitmq_connection()
#     channel = connection.channel()
#
#     channel.exchange_declare(
#         exchange='foodgram_tasks',
#         exchange_type='direct',
#         durable=True
#     )
#
#     # Создаём очередь (durable)
#     channel.queue_declare(queue=queue_name, durable=True)
#
#     # Привязываем очередь к exchange с routing_key = имя очереди
#     channel.queue_bind(exchange='foodgram_tasks', queue=queue_name, routing_key=queue_name)
#
#     channel.basic_qos(prefetch_count=1)
#     channel.basic_consume(queue=queue_name, on_message_callback=lambda ch, method, props, body: callback(ch, method, props, body, output_dir))
#
#     print(f' [*] Worker for queue "{queue_name}" started. Waiting for messages. To exit press CTRL+C')
#     channel.start_consuming()
