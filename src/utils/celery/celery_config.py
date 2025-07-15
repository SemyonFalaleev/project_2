from celery import Celery
from decouple import config

celery_app = Celery(
    "worker", broker=config("RABBITMQ_URL"), include=["src.utils.celery.celery_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Novosibirsk",
    enable_utc=True,
)
