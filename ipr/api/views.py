from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import QuerySet
from rest_framework import decorators, permissions, viewsets
from rest_framework.response import Response

from .permissions import IsAuthenticatedReadOnly
from .serializers import (
    CommentSerializer,
    CreateTaskSerializer,
    TaskSerializer,
    UserSerializer,
    CreateIprSerializer,
    ReadIprSerializer,
)
from iprs.models import Ipr, Task
from users.models import User


class UserViewSet(
    viewsets.ReadOnlyModelViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedReadOnly,)

    def get_object(self):
        if self.kwargs['pk'] == 'me':
            return self.request.user
        return super().get_object()

    @decorators.action(
        methods=('get',),
        detail=False,
    )
    def get_subordinates(self, request):
        user = request.user
        subordinates: QuerySet['User'] = user.subordinates.all()
        page = self.paginate_queryset(subordinates)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(subordinates, many=True)
        return Response(serializer.data)


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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskSerializer
        return CreateTaskSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs.get('task_id'))
        serializer.save(author=self.request.user, task=task)

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs.get('task_id'))
        return task.comments.all()
