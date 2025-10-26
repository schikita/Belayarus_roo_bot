# Берём лёгкий образ Python 3.12
FROM python:3.12-slim

# Обновим пакеты и установим зависимости для компиляции некоторых либ (если вдруг надо)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Укажем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем requirements.txt отдельно (чтобы слои кешировались)
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем весь проект внутрь контейнера
COPY . /app

# В контейнере .env не коммитим, мы будем прокидывать env через docker-compose
# но если хочешь можешь COPY .env /app/.env
# (лучше НЕ копировать .env в образ, чтобы не жёстко запекать токен в образ)

# Укажем переменную окружения для Python
ENV PYTHONUNBUFFERED=1

# Команда по умолчанию:
# Запуск твоего бота
CMD ["python", "-m", "main"]
