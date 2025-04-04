# DipProd - Диспетчер номенклатуры и ЛСИ

Этот репозиторий содержит два проекта:
1. **DipMain** - Django-приложение для управления номенклатурой и ЛСИ
2. **DipServer** - Java API-сервер для взаимодействия с базой данных

## Структура проекта

```
DipProd/
├── DipMain/              # Django-приложение (Frontend)
│   ├── Dip/              # Основной код Django-приложения
│   ├── Dockerfile        # Dockerfile для сборки Django-приложения
│   └── requirements.txt  # Зависимости Python
│
├── DipServer/            # Java API-сервер (Backend)
│   ├── python_api_server.py # Python-версия API-сервера
│   ├── Dockerfile        # Dockerfile для сборки API-сервера
│   └── pom.xml           # Зависимости Maven
│
├── config/               # Конфигурационные файлы
└── docs/                 # Документация проекта
```

## Режимы работы

Приложение поддерживает два режима:
- **Атом** - Работа с локальной базой данных
- **TeamCenter** - Работа с API TeamCenter

## Запуск проекта

Для запуска проекта используется Docker Compose:

```
docker-compose up -d
```

После запуска:
- Django-приложение доступно по адресу: http://localhost:8888
- API-сервер доступен по адресу: http://localhost:8081/api

## Авторы

- Редькин Иван Александрович, ТИП-72
