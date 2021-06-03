from django.shortcuts import redirect
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response

from core import models
from core import serializers
from core.utils.loader import load_forecasts_to_excel
from core.utils.pagination import CustomPagination


class ForecastViewSet(viewsets.ModelViewSet):
    queryset = models.Forecast.all()
    serializer_class = serializers.ForecastResponseSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        query_serializer=serializers.ForecastRequestSerializer(),
        responses={status.HTTP_200_OK: serializers.ForecastResponseSerializer(many=True)},
        operation_description='Use this method to get list of forecasts for specific city and/or timeline'
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = serializers.ForecastRequestSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        city = serializer.validated_data.get('city')
        start_time = serializer.validated_data.get('start_time')
        end_time = serializer.validated_data.get('end_time')
        download = serializer.validated_data.get('download', False)

        if city:
            if city.isnumeric():
                city_instance = models.City.get(id=int(city))
            else:
                city_instance = models.City.get(name=city)
            if city_instance:
                queryset = queryset.filter(city=city_instance)
        if start_time and end_time:
            queryset = queryset.filter(time__range=[start_time, end_time])

        if download:
            file_path = load_forecasts_to_excel(queryset)
            return redirect(to=file_path)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)


class CityViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    """
    Use this endpoint to get cities as paginated response. No filters available.
    """
    queryset = models.City.all()
    serializer_class = serializers.CitySerializer
    pagination_class = CustomPagination
