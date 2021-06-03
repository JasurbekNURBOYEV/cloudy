from django.contrib import admin

from core import models


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = [
        'id',
        'name',
        'country'
    ]
    search_fields = [
        'name',
    ]
    list_filter = [
        'country',
    ]

    exclude = [
        'created_time',
        'last_updated_time',
    ]


@admin.register(models.Forecast)
class ForecastAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = [
        'city',
        'detailed_status',
        'time'
    ]
    search_fields = [
        'name',
        'id'
    ]
    list_filter = [
        'city',
    ]

    exclude = [
        'created_time',
        'last_updated_time',
    ]

