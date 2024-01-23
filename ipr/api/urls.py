from django.urls import include, path
from rest_framework.routers import DefaultRouter

from comment.views import CommentViewSet
from task.views import TaskViewSet

router_v1 = DefaultRouter()
router_v1.register(
    'tasks', TaskViewSet,
    basename='task'
)
router_v1.register(
    r'tasks/(?P<task_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path("v1/", include(router_v1.urls)),]
