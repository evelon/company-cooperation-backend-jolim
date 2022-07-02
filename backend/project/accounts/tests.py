from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
import json


class TestAccountsViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        get_user_model().objects.user_create(
            username='username',
            password='password',
            email='email@example.com'
        )

    def test_registration_success(self):
        username = 'mockuser'
        password = 'strongpassword'
        email = 'eamil@email.com'
        response = self.client.post('/accounts/register', {
            'username': username,
            'password': password,
            'email': email,
        })
        # check status code
        self.assertEqual(response.status_code, 201)

        # check response
        content = json.loads(response.content)
        self.assertIn('id', content)
        self.assertIn('username', content)
        self.assertIn('email', content)

        # check if the user is created
        try:
            user = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist:
            self.assertTrue(False, msg='User is not created')
            return
        self.assertEqual(user.email, email)

    def test_registration_failure(self):
        username = 'too_long_username_too_long_username_too_long_username'
        password = 'short'
        email = 'invalid_email'
        response = self.client.post('/accounts/register', {
            'username': username,
            'password': password,
            'email': email,
        })
        # check status code
        self.assertEqual(response.status_code, 400)

        # check response
        content = json.loads(response.content)
        self.assertIn('username', content)
        self.assertIn('password', content)
        self.assertIn('email', content)
