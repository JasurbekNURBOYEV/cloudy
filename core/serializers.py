from rest_framework import serializers

from core import models


class ForecastRequestSerializer(serializers.Serializer):
    city = serializers.CharField(required=True, help_text='City name or city ID')
    start_time = serializers.DateTimeField(required=False, help_text='Starting time of forecasts')
    end_time = serializers.DateTimeField(required=False, help_text='Ending time of forecasts. Both start_date and '
                                                                   'end_date must be provided to filter by date.')
    download = serializers.BooleanField(required=False, default=False,
                                        help_text='If True, response will be as an excel file, otherwise, '
                                                  'paginated JSON response.')

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ForecastResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Forecast
        exclude = ('created_time', 'last_updated_time')


class CitySerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(queryset=models.Country.all(), slug_field='code')

    class Meta:
        model = models.City
        exclude = ('created_time', 'last_updated_time')
