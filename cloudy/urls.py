"""cloudy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg2 import openapi
from drf_yasg2.views import get_schema_view
from rest_framework.routers import DefaultRouter

from core.views import ForecastViewSet, CityViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Cloudy API",
        default_version='v1',
    ),
    public=False
)

router = DefaultRouter()

router.register(prefix='forecasts', viewset=ForecastViewSet)
router.register(prefix='cities', viewset=CityViewSet)

urlpatterns = [
    # API
    path('api/', include(router.urls)),
    # Admin panel
    path('admin/', admin.site.urls),
    # Docs
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]

if settings.DEBUG:
    # static files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
