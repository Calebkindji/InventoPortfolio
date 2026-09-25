from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.portfolios.models import Portfolio
from apps.projects.models import Project
from apps.skills.models import SkillCategory, Skill
from apps.experiences.models import Experience

User = get_user_model()


class PortfolioPlatformAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:token_obtain_pair')
        
        self.user_data = {
            "email": "jean.dupont@example.com",
            "username": "jeandupont",
            "first_name": "Jean",
            "last_name": "Dupont",
            "password": "StrongPassword123!",
            "password_confirm": "StrongPassword123!"
        }

    def test_full_user_workflow(self):
        # 1. Register User
        res = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', res.data)
        access_token = res.data['tokens']['access']

        # Set Auth Header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # 2. Update User Profile
        profile_url = reverse('profiles:profile_me')
        profile_res = self.client.patch(profile_url, {
            "title": "Développeur Full Stack Python / React",
            "bio": "Passionné par l'architecture logicielle et le web.",
            "location": "Lubumbashi, RDC",
            "github_url": "https://github.com/jeandupont"
        }, format='json')
        self.assertEqual(profile_res.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_res.data['title'], "Développeur Full Stack Python / React")

        # 3. Add Skill Category & Skill
        category = SkillCategory.objects.create(name="Backend", slug="backend")
        User.objects.filter(email=self.user_data['email']).update(is_staff=True)
        skill_url = reverse('skills:skill-list')
        skill_res = self.client.post(skill_url, {
            "name": "Django REST Framework",
            "category": category.id,
            "level": "EXPERT",
            "description": "Développement d'APIs REST modulaires"
        }, format='json')
        self.assertEqual(skill_res.status_code, status.HTTP_201_CREATED)

        skill_id = skill_res.data['id']
        profile_skill_url = reverse('skills:profile-skill-list')
        ps_res = self.client.post(profile_skill_url, {
            "skill": skill_id,
            "level": "EXPERT"
        }, format='json')
        self.assertEqual(ps_res.status_code, status.HTTP_201_CREATED)

        # 4. Add Experience
        exp_url = reverse('experiences:experience-list')
        exp_res = self.client.post(exp_url, {
            "position": "Lead Développeur Python",
            "company": "Tech Corp",
            "location": "Lubumbashi",
            "start_date": "2023-01-01",
            "is_current": True,
            "description": "Gestion de l'équipe backend."
        }, format='json')
        self.assertEqual(exp_res.status_code, status.HTTP_201_CREATED)

        # 5. Add Project
        project_url = reverse('projects:project-list')
        project_res = self.client.post(project_url, {
            "title": "Aura Player",
            "short_description": "Application mobile de lecture multimédia",
            "category": "Mobile",
            "status": "IN_PROGRESS",
            "progress_percentage": 70,
            "github_url": "https://github.com/jeandupont/aura-player"
        }, format='json')
        self.assertEqual(project_res.status_code, status.HTTP_201_CREATED)

        # 6. Publish Portfolio
        publish_url = reverse('portfolios:portfolio_publish')
        pub_res = self.client.post(publish_url)
        self.assertEqual(pub_res.status_code, status.HTTP_200_OK)
        self.assertEqual(pub_res.data['status'], "PUBLISHED")

        # 7. Unauthenticated Public Consultation
        self.client.credentials() # Clear credentials
        public_url = reverse('portfolios:public_portfolio', kwargs={'slug': 'jeandupont'})
        public_res = self.client.get(public_url)
        self.assertEqual(public_res.status_code, status.HTTP_200_OK)
        self.assertEqual(public_res.data['user_info']['username'], 'jeandupont')
        self.assertEqual(len(public_res.data['skills']), 1)
        self.assertEqual(len(public_res.data['projects']), 1)

        # 8. Record Visit & View Analytics
        visit_url = reverse('analytics:record_visit')
        portfolio_id = public_res.data['id']
        visit_res = self.client.post(visit_url, {"portfolio": portfolio_id}, format='json')
        self.assertEqual(visit_res.status_code, status.HTTP_201_CREATED)

        # 9. Search Endpoint
        search_url = reverse('exploration:global_search') + '?q=Aura'
        search_res = self.client.get(search_url)
        self.assertEqual(search_res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_res.data['projects']), 1)

        # 10. Content Report
        report_url = reverse('moderation:create_report')
        report_res = self.client.post(report_url, {
            "target_type": "PORTFOLIO",
            "target_id": portfolio_id,
            "reason": "Test de signalement"
        }, format='json')
        self.assertEqual(report_res.status_code, status.HTTP_201_CREATED)

    def test_social_and_exports_workflow(self):
        # Create User 1 (Author)
        user1 = User.objects.create_user(email="user1@example.com", username="user1", password="Password123!", first_name="User", last_name="One")
        project = Project.objects.create(user=user1, title="Test Project", short_description="Short desc")

        # Create User 2 (Visitor/Interacter)
        user2 = User.objects.create_user(email="user2@example.com", username="user2", password="Password123!", first_name="User", last_name="Two")

        self.client.force_authenticate(user=user2)

        # 1. Like Project
        like_url = reverse('social:toggle_project_like', kwargs={'project_id': project.id})
        like_res = self.client.post(like_url)
        self.assertEqual(like_res.status_code, status.HTTP_200_OK)
        self.assertTrue(like_res.data['is_liked'])

        # 2. Add Comment
        comment_url = reverse('social:project_comments', kwargs={'project_id': project.id})
        comment_res = self.client.post(comment_url, {"text": "Superbe projet ! Bravo."}, format='json')
        self.assertEqual(comment_res.status_code, status.HTTP_201_CREATED)

        # 3. Follow User
        follow_url = reverse('social:toggle_follow', kwargs={'user_id': user1.id})
        follow_res = self.client.post(follow_url)
        self.assertEqual(follow_res.status_code, status.HTTP_200_OK)
        self.assertTrue(follow_res.data['is_following'])

        # 4. Check Notifications for User 1
        self.client.force_authenticate(user=user1)
        notif_url = reverse('social:notifications')
        notif_res = self.client.get(notif_url)
        self.assertEqual(notif_res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(notif_res.data['results']), 3) # Like, Comment, Follow

        # 5. Export QR Code
        qr_url = reverse('exports:qrcode', kwargs={'username': 'user1'})
        qr_res = self.client.get(qr_url)
        self.assertEqual(qr_res.status_code, status.HTTP_200_OK)
        self.assertEqual(qr_res['Content-Type'], 'image/png')

        # 6. Export CV PDF
        cv_url = reverse('exports:export_cv_pdf', kwargs={'username': 'user1'})
        cv_res = self.client.get(cv_url)
        self.assertEqual(cv_res.status_code, status.HTTP_200_OK)
        self.assertEqual(cv_res['Content-Type'], 'application/pdf')

