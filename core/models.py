from django.contrib.postgres.fields import JSONField
from django.db import models

from core.utils.time import get_now


class BaseManager(models.Manager):
    """
    Our basic manager is used to order all child models of AbstractLayer
    by created time (descending), therefore it creates a LIFO order,
    causing the recent ones appear first in results.
    """
    use_for_related_fields = True

    def get_queryset(self):
        super(BaseManager, self).get_queryset().order_by('-created_time')


class AbstractLayer(models.Model):
    """
    All basic abstraction is done here.
    Also, we'll implement some methods which will simplify the work with models.
    """

    # let's configure managers
    default_manager = BaseManager
    objects = BaseManager
    all_objects = models.Manager

    # All objects in our database are gonna have time of creation and last updated time.
    created_time = models.DateTimeField(default=get_now)
    last_updated_time = models.DateTimeField(default=get_now)

    @classmethod
    def get(cls, *args, **kwargs) -> object or None:
        """
        We use our custom get method to avoid errors (like Not Found).
        This way we won't have to use try/except for the rest of our codebase (at least for non-existing objects).
        :param args:
        :param kwargs:
        :return: object of model
        """
        try:
            return cls.objects.get(*args, **kwargs)
        except cls.DoesNotExist:
            # if objects does not exist, we use None
            return None

    @classmethod
    def filter(cls, *args, **kwargs) -> models.QuerySet:
        """
        Just to reduce the model.objects.filter to model.filter
        :param args:
        :param kwargs:
        :return: QuerySet
        """
        return cls.objects.filter(*args, **kwargs)

    @classmethod
    def all(cls):
        """
        Shortcut for model.objects.all
        """
        return cls.objects.all()

    def save(self, *args, **kwargs) -> None:
        """
        We won't be using auto_now and auto_add_now for created_time and last_updated_time,
        since they might cause unintentional errors in future.
        Instead we implement custom save method to update them.
        :param args:
        :param kwargs:
        :return: None
        """
        self.last_updated_time = get_now()
        super(AbstractLayer, self).save(*args, **kwargs)

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Since we are not using auto fields for created_time,
        we will be implementing our custom create method to take care of that.
        Also, we reduce model.objects.create to model.create.
        :param args:
        :param kwargs:
        :return: created object
        """
        now = get_now()
        obj = cls(
            *args,
            **kwargs,
            created_time=now,
            last_updated_time=now
        )
        obj.save()
        return obj

    class Meta:
        abstract = True


class Country(AbstractLayer):
    code = models.CharField(max_length=7, unique=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'countries'


class City(AbstractLayer):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    lon = models.CharField(max_length=31)
    lat = models.CharField(max_length=31)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cities'


class Forecast(AbstractLayer):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='forecasts')
    detailed_status = models.CharField(max_length=1023, blank=True, null=True)
    data = JSONField(blank=True, null=True, help_text='Whole JSON data representing the forecast details')
    time = models.DateTimeField()

    class Meta:
        db_table = 'forecasts'
