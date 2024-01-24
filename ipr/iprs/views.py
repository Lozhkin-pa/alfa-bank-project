from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Ipr
from .serializers import CreateIprSerializer, ReadIprSerializer
from django_filters.rest_framework import DjangoFilterBackend


class IprViewSet(viewsets.ModelViewSet):
    queryset = Ipr.objects.all()
    permission_classes = (IsAuthenticated,)
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
