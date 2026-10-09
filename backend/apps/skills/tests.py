from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.skills.models import SkillCategory, Skill, ProfileSkill
from apps.profiles.models import UserProfile

User = get_user_model()


class SkillsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = SkillCategory.objects.create(name="Backend", slug="backend")
        self.skill = Skill.objects.create(name="Python", category=self.category)
        self.user = User.objects.create_user(
            email="skillsuser@invento.com",
            username="skillsuser",
            password="StrongPassword123!",
            first_name="Skills",
            last_name="User"
        )
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user)

    def test_list_skills_public(self):
        url = reverse('skills:skill-list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)

    def test_add_profile_skill(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('skills:profile-skill-list')
        payload = {
            "skill": self.skill.id,
            "level": "EXPERT"
        }
        res = self.client.post(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProfileSkill.objects.filter(profile=self.profile).count(), 1)
