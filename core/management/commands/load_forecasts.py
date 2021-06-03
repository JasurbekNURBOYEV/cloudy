from django.core.management.base import BaseCommand

from core.utils.loader import load_forecasts_from_api


class Command(BaseCommand):
    help = "We'll use this command to run sync process manually (whenever necessary)"

    def handle(self, *args, **options):
        load_forecasts_from_api()
