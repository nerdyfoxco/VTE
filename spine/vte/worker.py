import os
from celery import Celery

# Get config from Env (set in docker-compose)
BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "vte_worker",
    broker=BROKER_URL,
    backend=BACKEND_URL,
    include=["vte.tasks"] # We will create this next
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
