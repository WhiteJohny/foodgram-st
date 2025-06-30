# Базовый образ
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создание директорий для статических и медиа файлов
RUN mkdir -p /app/static /app/media

RUN chmod +x /app/entrypoint.sh

# Установка переменных окружения
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=foodgram.settings

# Запуск entrypoint скрипта
ENTRYPOINT ["/app/entrypoint.sh"]
