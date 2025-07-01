# Foodgram - Смотрите и делитесь рецептами!

Ссылка на репозиторий: https://github.com/WhiteJohny/foodgram-st/

## Запуск проекта

### Требования

- Docker
- Docker Compose
- Git

### 1. Клонирование репозитория

```bash
git clone https://github.com/WhiteJohny/foodgram-st/
cd foodgram-st
```

### 2. Настройка .env

Создайте файл .env (та же папка, где находится и 
docker-compose.yml)

```
# Django
SECRET_KEY=django-insecure-q*)7tnare(0#d_=0dwhe13@*#(@k%oyflyih9xwz61vh)5)_fm
DB_ENGINE=django.db.backends.postgresql
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,backend,host.docker.internal
DJANGO_SUPERUSER_EMAIL=admin@gmail.com
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_FIRST_NAME=Vasya
DJANGO_SUPERUSER_LAST_NAME=Pupkin
DJANGO_SUPERUSER_PASSWORD=Pupkin228

# PostgreSQL
DB_PASSWORD=password
DB_USER=user
DB_NAME=db_name
DB_HOST=db
DB_PORT=5432

# Static Files
STATIC_ROOT=/app/static
MEDIA_ROOT=/app/media
```

### 3. Запуск docker-compose.yml

Находясь в foodgram-st/, выполните следюущее:
```bash
docker-compose up --build
```

В вашем распоряжении будут 2 обычных пользователя и суперпользователь 
admin@gmail.com.

Вот их данные для входа:
```
admin@gmail.com
Pupkin228

sprut@gmail.com
Sprut123

sanchez@gmail.com
Sanchez123
```