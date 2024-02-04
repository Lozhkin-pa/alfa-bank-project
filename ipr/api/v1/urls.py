from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from api import views


v1_router = DefaultRouter()
v1_router.register('iprs/my', views.MyIprViewSet, basename='my_iprs')
v1_router.register('iprs/subordinates', views.IprViewSet, basename='iprs')
v1_router.register('users', views.UserViewSet, basename='users')
v1_router.register(
    r'tasks/(?P<task_id>\d+)/comments',
    views.CommentViewSet,
    basename='comment'
)
v1_router.register(
    r'iprs/(?P<ipr_id>\d+)/tasks',
    views.TaskViewSet,
    basename='task'
)

urlpatterns = [
    path('auth/', obtain_auth_token, name='auth'),
    path('', include(v1_router.urls)),
]