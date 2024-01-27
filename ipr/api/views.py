from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, authentication, permissions, viewsets

from .filters import TaskFilter
from .permissions import IsAdminOrSelf, IsAuthenticatedReadOnly
from .serializers import CommentSerializer, CreateTaskSerializer, TaskSerializer, UserSerializer, CreateIprSerializer, \
    ReadIprSerializer, UpdateTaskSerializer
from iprs.models import Ipr, Task
from users.models import User


class UserList(generics.ListCreateAPIView):  # используй viewsets
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAdminUser,)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (
        IsAdminOrSelf,
        IsAuthenticatedReadOnly,
    )


class IprViewSet(viewsets.ModelViewSet):
    queryset = Ipr.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('status', 'end_date',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadIprSerializer
        return CreateIprSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """
        Если руководитель/подчиненный определяется в модели User типом bool:
        """
        if self.request.user.superior:
            return Ipr.objects.filter(author=self.request.user)
        if self.request.user.subordinates:
            return Ipr.objects.filter(employee=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTaskSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateTaskSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        ipr = get_object_or_404(Ipr, id=self.kwargs.get('ipr_id'))
        serializer.save(author=self.request.user, ipr=ipr)

    def get_queryset(self):
        ipr = get_object_or_404(Ipr, id=self.kwargs.get('ipr_id'))
        return ipr.tasks_ipr.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs.get('task_id'))
        serializer.save(author=self.request.user, task=task)

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs.get('task_id'))
        return task.comments.all()
