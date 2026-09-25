from rest_framework import serializers
from .models import ProjectLike, ProjectComment, Follow, Notification
from apps.accounts.serializers import UserSerializer


class ProjectLikeSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ProjectLike
        fields = ('id', 'user', 'user_username', 'project', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')


class ProjectCommentSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = ProjectComment
        fields = ('id', 'user', 'user_detail', 'project', 'text', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'project', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class FollowSerializer(serializers.ModelSerializer):
    follower_username = serializers.CharField(source='follower.username', read_only=True)
    followed_username = serializers.CharField(source='followed.username', read_only=True)

    class Meta:
        model = Follow
        fields = ('id', 'follower', 'follower_username', 'followed', 'followed_username', 'created_at')
        read_only_fields = ('id', 'follower', 'created_at')


class NotificationSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'sender', 'sender_username', 'notification_type', 'message', 'target_url', 'is_read', 'created_at')
        read_only_fields = ('id', 'recipient', 'sender', 'created_at')
