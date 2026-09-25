from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:token_obtain_pair')
        self.me_url = reverse('accounts:user_me')
        self.change_password_url = reverse('accounts:change_password')

        self.user_data = {
            "email": "testuser@invento.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "SecurePassword123!",
            "password_confirm": "SecurePassword123!"
        }

    def test_user_registration_success(self):
        res = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', res.data)
        self.assertIn('access', res.data['tokens'])
        self.assertIn('refresh', res.data['tokens'])
        self.assertEqual(res.data['user']['email'], self.user_data['email'])

    def test_user_login_success(self):
        User.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],
            password=self.user_data['password'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name']
        )
        login_data = {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        }
        res = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_change_password(self):
        user = User.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],
            password=self.user_data['password'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name']
        )
        self.client.force_authenticate(user=user)
        payload = {
            "old_password": "SecurePassword123!",
            "new_password": "NewSecurePassword456!",
            "new_password_confirm": "NewSecurePassword456!"
        }
        res = self.client.post(self.change_password_url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(user.check_password("NewSecurePassword456!"))
