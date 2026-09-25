from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.portfolios.models import Portfolio

User = get_user_model()


class PortfolioAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.check_slug_url = reverse('portfolios:check_slug')
        self.user = User.objects.create_user(
            email="jean.test@invento.com",
            username="jeantest",
            password="StrongPassword123!",
            first_name="Jean",
            last_name="Test"
        )
        self.portfolio, _ = Portfolio.objects.get_or_create(user=self.user)

    def test_check_slug_available(self):
        res = self.client.get(f"{self.check_slug_url}?slug=nouveau-slug-libre")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['is_available'])
        self.assertEqual(res.data['slug'], 'nouveau-slug-libre')

    def test_check_slug_taken(self):
        res = self.client.get(f"{self.check_slug_url}?slug=jeantest")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Unauthenticated user checking existing slug
        self.assertFalse(res.data['is_available'])

    def test_check_slug_own_slug(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get(f"{self.check_slug_url}?slug=jeantest")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Authenticated user checking their own slug
        self.assertTrue(res.data['is_available'])
