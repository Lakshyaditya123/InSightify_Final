from celery import Celery
from InSightify.Common_files.config import config


app = Celery(
    "InSightify_tasks",
    broker = config.REDDIS_URL,
)
app.conf.task_routes = {
    "tags_worker":{
        "queue":"tags_worker"
    },
    "merge_idea_worker":{
        "queue":"merge_idea_worker"
    }
}


app.autodiscover_tasks(["InSightify.celery_server.Celery_tasks"])