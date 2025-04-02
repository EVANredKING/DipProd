# Java HTTP Сервер

Простой HTTP-сервер на Java с реализацией REST API.

## Требования

- Java 22
- Maven

## Запуск сервера

1. Клонируйте репозиторий
2. Перейдите в корневую директорию проекта
3. Соберите проект с помощью Maven:

```bash
mvn clean package
```

4. Запустите сервер:

```bash
java -jar target/DipServer-1.0-SNAPSHOT.jar
```

Сервер будет запущен на порту 8080.

## Доступные API endpoints

### Общие эндпоинты

- `GET /` - Главная страница
- `GET /api/status` - Получить статус сервера
- `GET /api/info` - Получить информацию о сервере
- `POST /api/echo` - Эхо-сервис, возвращает переданные данные
- `POST /api/submit` - Сервис приема данных

### API пользователей

- `GET /api/users` - Получить список всех пользователей
- `GET /api/users/{id}` - Получить пользователя по ID
- `POST /api/users` - Создать нового пользователя
- `PUT /api/users/{id}` - Обновить данные пользователя
- `DELETE /api/users/{id}` - Удалить пользователя

## Примеры запросов

### Получение списка пользователей

```bash
curl -X GET http://localhost:8080/api/users
```

### Создание нового пользователя

```bash
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "email": "newuser@example.com"}'
```

### Обновление данных пользователя

```bash
curl -X PUT http://localhost:8080/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"username": "updateduser", "email": "updated@example.com"}'
```

### Удаление пользователя

```bash
curl -X DELETE http://localhost:8080/api/users/1
```

## Структура проекта

- `src/main/java/org/example/Main.java` - Точка входа приложения, настройка HTTP-сервера
- `src/main/java/org/example/controller/` - Контроллеры для обработки HTTP-запросов
- `src/main/java/org/example/model/` - Модели данных
- `src/main/java/org/example/service/` - Сервисы для работы с данными 