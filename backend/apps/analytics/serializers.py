from rest_framework import serializers
from .models import PortfolioVisit, ProjectView, LinkClick


class PortfolioVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioVisit
        fields = ('id', 'portfolio', 'visited_at', 'ip_address', 'referrer', 'user_agent')
        read_only_fields = ('id', 'visited_at')


class ProjectViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectView
        fields = ('id', 'project', 'viewed_at')
        read_only_fields = ('id', 'viewed_at')


class LinkClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkClick
        fields = ('id', 'portfolio', 'link_type', 'target_url', 'clicked_at')
        read_only_fields = ('id', 'clicked_at')
