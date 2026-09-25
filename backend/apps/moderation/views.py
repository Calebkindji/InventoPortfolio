from rest_framework import generics, permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import ContentReport
from .serializers import ContentReportSerializer, AdminUserManagementSerializer
from apps.core.permissions import IsAdminUserRole
from apps.portfolios.models import Portfolio
from apps.projects.models import Project
from apps.analytics.models import PortfolioVisit

User = get_user_model()


class CreateContentReportView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ContentReportSerializer


class AdminReportViewSet(viewsets.ModelViewSet):
    queryset = ContentReport.objects.all()
    serializer_class = ContentReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserRole]


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = AdminUserManagementSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserRole]


class AdminGlobalStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserRole]

    def get(self, request, *args, **kwargs):
        total_users = User.objects.count()
        total_portfolios = Portfolio.objects.count()
        published_portfolios = Portfolio.objects.filter(status=Portfolio.Status.PUBLISHED).count()
        total_projects = Project.objects.count()
        total_visits = PortfolioVisit.objects.count()

        return Response({
            'total_users': total_users,
            'total_portfolios': total_portfolios,
            'published_portfolios': published_portfolios,
            'total_projects': total_projects,
            'total_visits': total_visits,
        })
