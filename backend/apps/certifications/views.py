from rest_framework import viewsets, permissions
from .models import Certification
from .serializers import CertificationSerializer
from apps.core.permissions import IsOwnerOrReadOnly


class CertificationViewSet(viewsets.ModelViewSet):
    serializer_class = CertificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Certification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
