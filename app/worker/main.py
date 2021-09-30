from celery import Celery
from celery.utils.log import get_task_logger

from app.core.settings import settings


celery = Celery(
    __name__,
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[]
)
celery.conf.update(
    result_expires=7200,
    task_ignore_result=False,
    task_track_started=True,
)

celery_log = get_task_logger(__name__)
celery.autodiscover_tasks()