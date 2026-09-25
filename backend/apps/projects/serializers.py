from rest_framework import serializers
from .models import Project, ProjectSkill, ExternalLink, Media, ProjectMedia
from apps.skills.serializers import SkillSerializer


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = (
            'id', 'storage_key', 'url', 'mime_type', 'size',
            'alt_text', 'media_type', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class ExternalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalLink
        fields = ('id', 'profile', 'project', 'url', 'label', 'type', 'order', 'created_at')
        read_only_fields = ('id', 'profile', 'created_at')

    def validate_url(self, value):
        if not value.lower().startswith(('http://', 'https://')):
            raise serializers.ValidationError('Seules les URLs HTTP et HTTPS sont autorisées.')
        return value


class ProjectSkillSerializer(serializers.ModelSerializer):
    skill_detail = SkillSerializer(source='skill', read_only=True)

    class Meta:
        model = ProjectSkill
        fields = ('id', 'project', 'skill', 'skill_detail', 'created_at')
        read_only_fields = ('id', 'created_at')


class ProjectMediaSerializer(serializers.ModelSerializer):
    media = MediaSerializer(read_only=True)

    class Meta:
        model = ProjectMedia
        fields = ('id', 'project', 'media', 'order', 'created_at')
        read_only_fields = ('id', 'created_at')


class ProjectSerializer(serializers.ModelSerializer):
    media_gallery = ProjectMediaSerializer(many=True, read_only=True)
    skills = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'user', 'title', 'short_description', 'detailed_description',
            'main_image', 'category', 'status', 'status_display',
            'progress_percentage', 'technologies_used', 'start_date', 'end_date',
            'role', 'is_featured', 'order', 'skills', 'links', 'media_gallery',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def get_skills(self, obj):
        return SkillSerializer(
            [relation.skill for relation in obj.project_skills.all()],
            many=True, context=self.context
        ).data

    def get_links(self, obj):
        links = obj.external_links.all()
        return ExternalLinkSerializer(links, many=True, context=self.context).data

    def validate(self, attrs):
        start = attrs.get('start_date', getattr(self.instance, 'start_date', None))
        end = attrs.get('end_date', getattr(self.instance, 'end_date', None))
        if start and end and end < start:
            raise serializers.ValidationError({'end_date': 'La date de fin doit être postérieure ou égale à la date de début.'})
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
