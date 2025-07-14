from src.utils.celery.celery_config import celery_app
from celery.schedules import schedule

celery_app.conf.beat_schedule = {
    'clean-inactive-users': {
        'task': 'clean_unconfirmed_users',
        'schedule': schedule(run_every=60*60),
    },
}