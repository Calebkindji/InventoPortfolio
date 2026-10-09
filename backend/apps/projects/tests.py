from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.projects.models import Project, ExternalLink, ProjectSkill
from apps.skills.models import Skill, SkillCategory

User = get_user_model()


class ProjectsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="dev@invento.com",
            username="devuser",
            password="StrongPassword123!",
            first_name="Dev",
            last_name="User"
        )
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse('projects:project-list')

    def test_create_and_list_project(self):
        payload = {
            "title": "Plateforme INVENTO",
            "short_description": "Plateforme de gestion de portfolios",
            "category": "Web",
            "status": "IN_PROGRESS",
            "progress_percentage": 60,
            "github_url": "https://github.com/invento/backend"
        }
        res = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], "Plateforme INVENTO")

        # List
        res_list = self.client.get(self.list_url)
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_list.data['results']), 1)

    def test_filter_project_by_status(self):
        Project.objects.create(
            user=self.user,
            title="Projet A",
            short_description="Desc A",
            status=Project.Status.COMPLETED
        )
        Project.objects.create(
            user=self.user,
            title="Projet B",
            short_description="Desc B",
            status=Project.Status.DRAFT
        )

        res = self.client.get(f"{self.list_url}?status=COMPLETED")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['title'], "Projet A")

    def test_add_external_link(self):
        project = Project.objects.create(
            user=self.user,
            title="Projet C",
            short_description="Desc C"
        )
        link_url = reverse('projects:external-link-list')
        payload = {
            "project": project.id,
            "url": "https://demo.invento.com",
            "label": "Démonstration Live",
            "type": "DEMO"
        }
        res = self.client.post(link_url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExternalLink.objects.count(), 1)

    def test_completed_project_auto_progress(self):
        payload = {
            "title": "Projet Terminé Auto Progress",
            "short_description": "Projet avec statut COMPLETED",
            "status": "COMPLETED",
            "progress_percentage": 50
        }
        res = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['progress_percentage'], 100)

    def test_max_featured_projects_limit(self):
        for i in range(5):
            Project.objects.create(
                user=self.user,
                title=f"Projet Featured #{i+1}",
                short_description="Description",
                is_featured=True
            )

        payload = {
            "title": "Projet Featured #6 Excédentaire",
            "short_description": "Devrait échouer",
            "is_featured": True
        }
        res = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("is_featured", res.data)
