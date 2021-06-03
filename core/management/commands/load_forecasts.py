from django.core.management.base import BaseCommand

from core.utils.loader import load_forecasts_from_api


class Command(BaseCommand):
    help = "We'll try to mimic celery task, and use this command to check if emails work"

    def handle(self, *args, **options):
        load_forecasts_from_api()
