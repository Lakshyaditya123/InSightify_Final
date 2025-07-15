from celery import Celery



app = Celery(
    "InSightify_tasks",
    broker = "redis://:12345@localhost:6379/0",  # or use host.docker.internal if calling from a container
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