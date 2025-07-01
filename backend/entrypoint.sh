#!/bin/bash

# Функция для проверки доступности PostgreSQL
wait_for_postgres() {
    echo "Waiting for postgres..."
    while ! nc -z db 5432; do
        sleep 0.1
    done
    echo "PostgreSQL started"
}

# Функция для применения миграций
apply_migrations() {
    echo "Applying database migrations..."
    python manage.py migrate
}

# Функция для сбора статических файлов
collect_static() {
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
}

load_ingredients() {
    echo "Loading ingredients..."
    python manage.py load_ingredients
    echo "Ingredients loaded "
}

# Функция для создания суперпользователя, если его нет
create_superuser() {
    if [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "Creating superuser..."
        python manage.py createsuperuser --noinput \
            --email $DJANGO_SUPERUSER_EMAIL \
            --username $DJANGO_SUPERUSER_USERNAME \
            --first_name $DJANGO_SUPERUSER_FIRST_NAME \
            --last_name $DJANGO_SUPERUSER_LAST_NAME
    fi
}

# Основной процесс
wait_for_postgres
apply_migrations
collect_static
load_ingredients
create_superuser

# Создаем пользователей через Django shell
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

# Первый пользователь
user1_email="sprut@gmail.com"
user1_username="sprut"
user1_password="Sprut123"

if not User.objects.filter(email=user1_email).exists():
    User.objects.create_user(
        email=user1_email,
        username=user1_username,
        password=user1_password,
        first_name="Вячеслав",
        last_name="Андреев"
    )
    print(f"Пользователь {user1_email} создан")
else:
    print(f"Пользователь {user1_email} уже существует")

# Второй пользователь
user2_email="sanchez@gmail.com"
user2_username="sanchez"
user2_password="Sanchez123"

if not User.objects.filter(email=user2_email).exists():
    User.objects.create_user(
        email=user2_email,
        username=user2_username,
        password=user2_password,
        first_name="Петр",
        last_name="Семенов"
    )
    print(f"Пользователь {user2_email} создан")
else:
    print(f"Пользователь {user2_email} уже существует")
EOF

echo "Created!"

# Запуск Gunicorn
echo "Starting Gunicorn..."
exec gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
