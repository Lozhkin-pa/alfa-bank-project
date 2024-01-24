from django.urls import path, include
from rest_framework.routers import DefaultRouter
from iprs.views import IprViewSet


v1_router = DefaultRouter()
v1_router.register('iprs', IprViewSet, basename='iprs')

urlpatterns = [
    path('', include(v1_router.urls)),
]