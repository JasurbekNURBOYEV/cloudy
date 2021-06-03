from celery.schedules import crontab

from cloudy.celery import app
from core.utils.loader import load_forecasts_from_api


@app.task
def sync():
    load_forecasts_from_api()


app.conf.beat_schedule = {
    # Schedule periodic task: every 10 minutes
    'run_pending_tasks': {
        'task': 'core.tasks.sync',
        'schedule': crontab(minute='*/10'),
    }
}
