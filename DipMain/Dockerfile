FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов проекта
COPY Dip/ /app/Dip/

# Создание директорий для статических и медиа файлов
RUN mkdir -p /app/Dip/static /app/Dip/media

# Сбор статических файлов
RUN cd Dip && python manage.py collectstatic --noinput

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["python", "Dip/waitress_server.py"] 