FROM openjdk:17-jdk-slim

WORKDIR /app

# Установка необходимых пакетов
RUN apt-get update && \
    apt-get install -y sqlite3 python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Создание директории для базы данных
RUN mkdir -p /app/database

# Копирование Python API сервера
COPY python_api_server.py /app/api_server.py

# Инициализация SQLite базы данных
RUN echo "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT);" > /app/init.sql

# Создание скрипта запуска
RUN echo '#!/bin/sh' > /app/run.sh && \
    echo 'cd /app' >> /app/run.sh && \
    echo 'sqlite3 /app/database.db < /app/init.sql' >> /app/run.sh && \
    echo 'python3 /app/api_server.py' >> /app/run.sh && \
    chmod +x /app/run.sh

EXPOSE 8081

CMD ["/app/run.sh"] 