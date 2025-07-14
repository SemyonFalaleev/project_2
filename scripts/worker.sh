#!/bin/bash
celery -A ../src.utils.celery.celery_config worker --loglevel=info