from src.utils.celery.celery_config import celery_app
from datetime import datetime
from src.db.sync_db.sync_func import _delete_unconfirmed_users
from src.tools.sender_email import send_email_token
from decouple import config

@celery_app.task
def sender_email_task(token, email: str, url_confirm):
    send_email_token(token, email, url_confirm, config("EMAIL_SENDER"),
                     config("EMAIL_SERVER_ADDR"), int(config("EMAIL_SERVER_PORT")),
                     config("PASSWD_EMAIL_SENDER"))

@celery_app.task(name="clean_unconfirmed_users")
def clean_unconfirmed_users():
    _delete_unconfirmed_users()
    print(f"🧹 Cleaning inactive users at {datetime.now()}")