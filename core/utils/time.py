from datetime import datetime

from django.utils import timezone


def get_now():
    return timezone.now().replace(tzinfo=timezone.get_current_timezone())


def timestamp_to_datetime(tmstmp: int) -> datetime:
    return datetime.fromtimestamp(tmstmp).replace(tzinfo=timezone.get_current_timezone())
