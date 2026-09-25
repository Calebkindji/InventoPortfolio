from rest_framework import serializers
from .models import ContentReport
from django.contrib.auth import get_user_model

User = get_user_model()


class ContentReportSerializer(serializers.ModelSerializer):
    reporter_username = serializers.CharField(source='reporter.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    target_type_display = serializers.CharField(source='get_target_type_display', read_only=True)

    class Meta:
        model = ContentReport
        fields = (
            'id', 'reporter', 'reporter_username', 'target_type',
            'target_type_display', 'target_id', 'reason', 'status',
            'status_display', 'admin_notes', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'reporter', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context['request'].user
        if user and user.is_authenticated:
            validated_data['reporter'] = user
        return super().create(validated_data)


class AdminUserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'role', 'is_active', 'is_suspended', 'created_at')
        read_only_fields = ('id', 'created_at')
