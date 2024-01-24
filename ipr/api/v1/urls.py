from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from api import views


v1_router = DefaultRouter()
v1_router.register('iprs', views.IprViewSet, basename='iprs')
v1_router.register(
    'tasks', views.TaskViewSet,
    basename='task'
)
v1_router.register(
    r'tasks/(?P<task_id>\d+)/comments',
    views.CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('', include(v1_router.urls)),
]