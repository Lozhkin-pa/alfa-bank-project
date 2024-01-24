from rest_framework import generics, authentication, permissions
from django.contrib.auth import get_user_model
from ..api.permissions import IsAdminOrSelf, IsAuthenticatedReadOnly
from ..api.serializers import UserSerializer

UserModel = get_user_model()


class UserList(generics.ListCreateAPIView):
    queryset = UserModel._default_manager.all()
    serializer_class = UserSerializer
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAdminUser,)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserModel._default_manager.all()
    serializer_class = UserSerializer
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (
        IsAdminOrSelf,
        IsAuthenticatedReadOnly,
    )
