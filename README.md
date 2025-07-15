# Project 2
[Ссылка на тестовое задание](https://docs.google.com/document/d/1U9Ps-ItyAgiz95-KuvSiHmmHyiLnneVAXZsMaxHu3UA/edit?tab=t.0)

## Содержание
- [О проекте](#о-проекте)
- [Реализованные фичи](#реализованные-фичи)
- [Структура](#структура)
- [Требования](#требования)
- [Установка](#установка)
- [Запуск](#запуск)
- [Переменные окружения](#переменные-окружения)
- [Структура permission.json](#структура-permission.json)
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
- Авторизация/Аутентификация через jwt-token. Токен храниться в cookie. Реализованна модель доступа RBAC.


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
```
При первом запуске проекта создаются роли в БД.

```
1 | user
2 | author
3 | admin
```

## Запуск

```bash
docker-compose up --build
```

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Переменные окружения

Смотри `.env.example`. Для переменных секретов и API-ключей используй `.env`.

## Структура permission.json
!Все пользователи создаются по дефолту с ролью 1!

Структура файла:
```
{
  "id роли": {
    "/path-to-router": [Methods list]}
}
```
Пример:
```
{
  "1": {
    "/category": ["GET", "POST", "PATCH", "DELETE"],
    "/category/{*}": ["GET", "DELETE", "POST"],
    "/user": ["GET", "POST"],
    "/article": ["GET", "POST", "PATCH", "DELETE"],
    "/article/{*}": ["GET", "DELETE"]}
}
```

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

