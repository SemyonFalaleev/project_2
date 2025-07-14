#!/bin/bash
celery -A ../src.utils.celery.celery_shedule beat --loglevel=info