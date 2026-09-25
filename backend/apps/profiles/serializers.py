from rest_framework import serializers
from .models import UserProfile
from apps.accounts.serializers import UserSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'user_detail', 'first_name', 'last_name',
            'profile_picture', 'title', 'bio', 'location',
            'professional_email', 'phone_number', 'website_url',
            'github_url', 'gitlab_url', 'linkedin_url', 'other_links',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')

        if first_name is not None or last_name is not None:
            user = instance.user
            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name
            user.save()

        return super().update(instance, validated_data)


class PublicProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'first_name', 'last_name', 'profile_picture',
            'title', 'bio', 'location', 'website_url', 'github_url',
            'gitlab_url', 'linkedin_url', 'other_links'
        )
        read_only_fields = fields
