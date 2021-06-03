from django.core.management.base import BaseCommand

from core.utils.loader import load_cities_from_json


class Command(BaseCommand):
    help = "We'll use this command to load cities from JSON to database"

    def handle(self, *args, **options):
        load_cities_from_json()
