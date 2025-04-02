# Настройка Nginx и Waitress для проекта

## Установка необходимых компонентов

### 1. Установка Waitress

```bash
pip install waitress
```

Или используйте файл requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Установка Nginx

#### Windows

1. Скачайте Nginx для Windows с официального сайта: https://nginx.org/en/download.html
2. Распакуйте в удобное место (например, C:\nginx)
3. Скопируйте файл nginx.conf из проекта в папку C:\nginx\conf\

#### Linux

```bash
sudo apt update
sudo apt install nginx
sudo cp nginx.conf /etc/nginx/nginx.conf
```

## Запуск проекта

### 1. Запуск Django с Waitress

```bash
cd DipMain/Dip
python waitress_server.py
```

### 2. Запуск Nginx

#### Windows

```bash
cd C:\nginx
start nginx
```

Для остановки:

```bash
nginx -s stop
```

Для перезагрузки конфигурации:

```bash
nginx -s reload
```

#### Linux

```bash
sudo systemctl start nginx
```

Для остановки:

```bash
sudo systemctl stop nginx
```

## Конфигурация

### Настройка Waitress

Файл `waitress_server.py` содержит основные настройки Waitress:
- host: 127.0.0.1 (локальный адрес)
- port: 8000 (порт для Django)
- threads: 4 (количество потоков)

Вы можете изменить эти параметры в соответствии с вашими потребностями.

### Настройка Nginx

Файл `nginx.conf` содержит конфигурацию Nginx:

#### Новые порты
- Django (Waitress): http://localhost:8888
- Java-сервер: http://localhost:9999

#### Прокси и маршрутизация
- Проксирование запросов к Django (Waitress) через http://127.0.0.1:8000
- Проксирование запросов к Java-серверу через http://127.0.0.1:8081
- Настройка статических файлов Django

Не забудьте заменить следующие параметры в конфигурации Nginx:
- `C:/Users/RED KING/PycharmProjects/DipMain/Dip/static/` — на реальный путь к статическим файлам
- `C:/Users/RED KING/PycharmProjects/DipMain/Dip/media/` — на реальный путь к медиа-файлам 