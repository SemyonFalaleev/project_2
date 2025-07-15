# Project 2
Ссылка на тестовое задание

## Содержание
- [О проекте](#о-проекте)
- [Структура](#структура)
- [Требования](#требования)
- [Установка](#установка)
- [Запуск](#запуск)
- [Переменные окружения](#переменные-окружения)
- [Скрипты](#скрипты)
- [Линтинг и стиль кода](#линтинг-и-стиль-кода)

---

## О проекте

REST API на FastAPI c PostgreSQL, Alembic, Celery, MinIO, RabbitMQ. Структурирован по `src-layout`.

## Реализованные фичи

- Когда пользователь регистрируется ему должно отсылаться электронное письмо на указанный почтовый адрес, чтобы подтвердить почту.(Celery + RabbitMQ).
- Каждый час sheduler проверят есть ли в бд пользователи , которые не подтвердили почту в течении одного дня. Если такие пользователи есть, то они удаляются, чтобы не захламлять БД.(Celery + RabbitMQ).
- Реализован поиск по фильтрам для статьей.
- Картинки для статей сохраняются в S3 хранилище Minio, общение с minio реализованно через библиотеку boto3 , которая совместима с другими S3 хранилищами, поэтому при желании можно изменить на другое хранилище.
- Реализованно фейковое удаление статей, статьи остаются в БД.
- При обновлении обложки статьи, старая обложка удаляется из S3.


## Структура

```
project\_2/
├── src/
│   ├── db/
│   ├── dto/
│   ├── handlers/
│   ├── models/
│   ├── utils/
│   └── main.py
├── migrations/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── .env.example
└── README.md
```

## Требования
- Python >= 3.13
- Docker + Docker Compose

## Установка

```bash
git clone git@github.com:<your_name>/project_2.git
cd project_2
cp .env.example .env
````

## Запуск

```bash
docker-compose up --build
```

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Переменные окружения

Смотри `.env.example`. Для переменных секретов и API-ключей используй `.env`.

## Скрипты

```bash
# Обновить базу данных
poetry run alembic upgrade head

# Запустить worker Celery
poetry run celery -A src.utils.celery.celery_config:celery_app worker --loglevel=info

# Запустить beat Celery
poetry run celery -A src.utils.celery.shedule:celery_app beat --loglevel=info
```

## Линтинг и стиль кода

```bash
# Проверка кода
poetry run ruff check .

# Форматировка
poetry run ruff format .

# С помощью pre-commit
pre-commit install
git commit -m "message"  # валидирует код
```

