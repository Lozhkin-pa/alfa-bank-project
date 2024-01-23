from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from .serializers import TaskSerializer, CreateTaskSerializer
from task.models import Task

CustomUser = get_user_model()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskSerializer
        return CreateTaskSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
