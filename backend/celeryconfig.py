import os

broker_url = os.environ.get('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672/foodgram')
result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'rpc://')
accept_content = os.environ.get('CELERY_ACCEPT_CONTENT', 'json').split(',')
task_serializer = os.environ.get('CELERY_TASK_SERIALIZER', 'json')
result_serializer = os.environ.get('CELERY_RESULT_SERIALIZER', 'json')
timezone = os.environ.get('CELERY_TIMEZONE', 'UTC')

task_queues = {
    'default': {
        'exchange': 'default',
        'routing_key': 'default',
    },
    'foodish': {
        'exchange': 'foodish',
        'routing_key': 'foodish',
    },
    'nyt': {
        'exchange': 'nyt',
        'routing_key': 'nyt',
    },
}

# Маршрутизация задач по очередям
task_routes = {
    'recipes.tasks.fetch_foodish_image': {'queue': 'foodish'},
    'recipes.tasks.fetch_nyt_article': {'queue': 'nyt'},
}
