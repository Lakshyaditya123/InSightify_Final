from celery import Celery
# from InSightify.celery_server import Celery_tasks


app = Celery(
    "InSightify_tasks",
    broker = "redis://:12345@localhost:6379/0",  # or use host.docker.internal if calling from a container
)
app.conf.task_routes = {
    "idea_worker":{
        "queue":"idea_worker"
    }
}

# # Optional: include task modules automatically
app.autodiscover_tasks(["InSightify.celery_server.Celery_tasks"])