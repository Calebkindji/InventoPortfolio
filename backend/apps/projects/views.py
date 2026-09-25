from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Project, ProjectMedia, ProjectSkill, ExternalLink
from .serializers import ProjectSerializer, ProjectMediaSerializer, ProjectSkillSerializer, ExternalLinkSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'is_featured']
    search_fields = ['title', 'short_description', 'detailed_description', 'category']
    ordering_fields = ['order', 'updated_at', 'created_at', 'progress_percentage']

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user).prefetch_related(
            'project_skills__skill__category', 'external_links', 'media_gallery__media'
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProjectMediaViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectMediaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectMedia.objects.filter(project__user=self.request.user).select_related('media', 'project')


class ProjectSkillViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectSkill.objects.filter(project__user=self.request.user).select_related('skill', 'project')

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        if project.user_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Vous ne pouvez modifier que vos propres projets.')
        serializer.save()


class ExternalLinkViewSet(viewsets.ModelViewSet):
    serializer_class = ExternalLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExternalLink.objects.filter(
            project__user=self.request.user
        ).select_related('project')

    def perform_create(self, serializer):
        project = serializer.validated_data.get('project')
        if not project or project.user_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Le lien doit appartenir à un de vos projets.')
        serializer.save()
