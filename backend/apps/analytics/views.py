from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import PortfolioVisit, ProjectView, LinkClick
from .serializers import PortfolioVisitSerializer, ProjectViewSerializer, LinkClickSerializer
from apps.portfolios.models import Portfolio
from apps.projects.models import Project


class RecordVisitView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PortfolioVisitSerializer

    def perform_create(self, serializer):
        ip = self.request.META.get('REMOTE_ADDR')
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        referrer = self.request.META.get('HTTP_REFERER', '')
        serializer.save(ip_address=ip, user_agent=user_agent, referrer=referrer)


class RecordProjectView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProjectViewSerializer


class RecordLinkClickView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LinkClickSerializer


class AnalyticsDashboardView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        portfolio = getattr(user, 'portfolio', None)

        if not portfolio:
            return Response({'detail': 'Aucun portfolio trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        total_visits = PortfolioVisit.objects.filter(portfolio=portfolio).count()
        total_project_views = ProjectView.objects.filter(project__user=user).count()

        top_projects = Project.objects.filter(user=user).annotate(
            view_count=Count('views')
        ).order_by('-view_count')[:5]

        link_clicks = LinkClick.objects.filter(portfolio=portfolio).values('link_type').annotate(
            count=Count('id')
        )

        return Response({
            'total_portfolio_visits': total_visits,
            'total_project_views': total_project_views,
            'top_projects': [
                {'id': p.id, 'title': p.title, 'views': p.view_count}
                for p in top_projects
            ],
            'link_clicks': list(link_clicks),
        })
