from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
)


app_name = 'api'

urlpatterns = [
    path('v1/', include('api.v1.urls')),
    path(
        'v1/schema/',
        SpectacularAPIView.as_view(api_version='api/v1'),
        name='schema'
    ),
    path(
        'v1/swagger/',
        SpectacularSwaggerView.as_view(url_name='api:schema'),
        name='swagger-ui',
    ),
    path(
        'v1/redoc/',
        SpectacularRedocView.as_view(url_name='api:schema'),
        name='redoc',
    ),
]
