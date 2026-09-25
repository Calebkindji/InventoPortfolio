from rest_framework import serializers
from .models import SkillCategory, Skill, ProfileSkill


class SkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = ('id', 'name', 'slug', 'description')
        read_only_fields = ('id',)


class SkillSerializer(serializers.ModelSerializer):
    category_detail = SkillCategorySerializer(source='category', read_only=True)

    class Meta:
        model = Skill
        fields = ('id', 'name', 'category', 'category_detail', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProfileSkillSerializer(serializers.ModelSerializer):
    skill_detail = SkillSerializer(source='skill', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)

    class Meta:
        model = ProfileSkill
        fields = (
            'id', 'profile', 'skill', 'skill_detail', 'level',
            'level_display', 'order', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'profile', 'created_at', 'updated_at')

    def validate_skill(self, value):
        profile = getattr(self.context.get('request'), 'user', None)
        if profile and ProfileSkill.objects.filter(profile__user=profile, skill=value).exclude(pk=getattr(self.instance, 'pk', None)).exists():
            raise serializers.ValidationError('Cette compétence est déjà associée à votre profil.')
        return value
