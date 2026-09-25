from rest_framework import viewsets, permissions
from .models import Experience
from .serializers import ExperienceSerializer
from apps.core.permissions import IsOwnerOrReadOnly


class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Experience.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
