from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from api import views


v1_router = DefaultRouter()
v1_router.register('iprs', views.IprViewSet, basename='iprs')
# v1_router.register('users/<int:pk>/', views.UserDetail, basename='users')

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('', include(v1_router.urls)),
]