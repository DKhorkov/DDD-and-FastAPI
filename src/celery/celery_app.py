from celery import Celery

from src.celery.celery_app_config import celery_app_config

celery = Celery('tasks')
celery.config_from_object(celery_app_config)
