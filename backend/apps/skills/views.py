from rest_framework import viewsets, permissions
from .models import SkillCategory, Skill, ProfileSkill
from .serializers import SkillCategorySerializer, SkillSerializer, ProfileSkillSerializer


class SkillCategoryViewSet(viewsets.ModelViewSet):
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.select_related('category').all()
    serializer_class = SkillSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class ProfileSkillViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProfileSkill.objects.filter(
            profile__user=self.request.user
        ).select_related('skill', 'skill__category', 'profile')

    def perform_create(self, serializer):
        from apps.profiles.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)
