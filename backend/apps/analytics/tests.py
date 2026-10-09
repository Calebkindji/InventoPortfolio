from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.portfolios.models import Portfolio
from apps.projects.models import Project
from apps.analytics.models import PortfolioVisit, ProjectView, LinkClick

User = get_user_model()


class AnalyticsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="analytics.user@invento.com",
            username="analyticsuser",
            password="StrongPassword123!",
            first_name="Analytics",
            last_name="User"
        )
        self.portfolio, _ = Portfolio.objects.get_or_create(user=self.user)
        self.project = Project.objects.create(
            user=self.user,
            title="Projet Analytics",
            short_description="Description court"
        )

    def test_record_visit(self):
        url = reverse('analytics:record_visit')
        res = self.client.post(url, {"portfolio": self.portfolio.id}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PortfolioVisit.objects.filter(portfolio=self.portfolio).count(), 1)

    def test_record_project_view(self):
        url = reverse('analytics:record_project_view')
        res = self.client.post(url, {"project": self.project.id}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProjectView.objects.filter(project=self.project).count(), 1)

    def test_analytics_dashboard(self):
        PortfolioVisit.objects.create(portfolio=self.portfolio)
        ProjectView.objects.create(project=self.project)
        LinkClick.objects.create(portfolio=self.portfolio, link_type='GITHUB', target_url='https://github.com/analyticsuser')

        self.client.force_authenticate(user=self.user)
        dashboard_url = reverse('analytics:dashboard')
        res = self.client.get(dashboard_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['total_portfolio_visits'], 1)
        self.assertEqual(res.data['total_project_views'], 1)
        self.assertEqual(len(res.data['top_projects']), 1)
