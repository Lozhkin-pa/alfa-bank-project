from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, authentication, permissions, viewsets

from .permissions import IsAdminOrSelf, IsAuthenticatedReadOnly
from .serializers import UserSerializer, CreateIprSerializer, ReadIprSerializer
from iprs.models import Ipr
from users.models import User


class UserList(generics.ListCreateAPIView): # используй viewsets
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
