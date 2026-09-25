from rest_framework import viewsets, permissions
from .models import Education
from .serializers import EducationSerializer
from apps.core.permissions import IsOwnerOrReadOnly


class EducationViewSet(viewsets.ModelViewSet):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
