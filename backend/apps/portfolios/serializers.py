from rest_framework import serializers
from .models import Portfolio
from apps.profiles.serializers import PublicProfileSerializer
from apps.skills.serializers import ProfileSkillSerializer
from apps.experiences.serializers import ExperienceSerializer
from apps.educations.serializers import EducationSerializer
from apps.certifications.serializers import CertificationSerializer
from apps.projects.serializers import ProjectSerializer


class PortfolioStateSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Portfolio
        fields = ('id', 'slug', 'status', 'status_display', 'custom_theme', 'published_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'status', 'published_at', 'updated_at')


class PublicPortfolioSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    experiences = serializers.SerializerMethodField()
    educations = serializers.SerializerMethodField()
    certifications = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = (
            'id', 'slug', 'status', 'custom_theme', 'published_at',
            'user_info', 'profile', 'skills', 'experiences',
            'educations', 'certifications', 'projects'
        )

    def get_user_info(self, obj):
        user = obj.user
        return {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.get_full_name(),
        }

    def get_profile(self, obj):
        profile = getattr(obj.user, 'profile', None)
        return PublicProfileSerializer(profile, context=self.context).data if profile else None

    def get_skills(self, obj):
        profile = getattr(obj.user, 'profile', None)
        if not profile:
            return []
        return ProfileSkillSerializer(
            profile.profile_skills.select_related('skill', 'skill__category').all(),
            many=True, context=self.context
        ).data

    def get_experiences(self, obj):
        return ExperienceSerializer(obj.user.experiences.all(), many=True, context=self.context).data

    def get_educations(self, obj):
        return EducationSerializer(obj.user.educations.all(), many=True, context=self.context).data

    def get_certifications(self, obj):
        return CertificationSerializer(obj.user.certifications.all(), many=True, context=self.context).data

    def get_projects(self, obj):
        projects = obj.user.projects.exclude(status='ARCHIVED')
        return ProjectSerializer(projects, many=True, context=self.context).data
