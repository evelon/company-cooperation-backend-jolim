from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
import json
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class TestAccountsViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        get_user_model().objects.create_user(
            username='username',
            password='password',
            email='email@example.com'
        )
        user = get_user_model().objects.get(username='username')
        self.tokens = get_tokens_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='bearer ' + self.tokens['access'])

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

    def test_issue_token_success(self):
        username = 'username'
        password = 'password'

        response = self.client.post('/accounts/token', {
            'username': username,
            'password': password,
        })
        # check status code
        self.assertEqual(response.status_code, 200)

        # check response
        content = json.loads(response.content)
        self.assertIn('access', content)
        self.assertIn('refresh', content)

    def test_issue_token_failure(self):
        username = 'random'
        password = 'wrong'

        response = self.client.post('/accounts/token', {
            'username': username,
            'password': password,
        }, format='json')
        self.assertEqual(response.status_code, 401)

    def test_token_verify_success(self):
        response = self.client.post('/accounts/token/verify', {
            'token': self.tokens['access']
        }, format='json')
        self.assertEqual(response.status_code, 200)

    def test_token_verify_failure(self):
        response = self.client.post('/accounts/token/verify', {
            'token': 'no_meaning'
        })
        self.assertEqual(response.status_code, 401)

    def test_token_refresh_success(self):
        response = self.client.post('/accounts/token/refresh', {
            'refresh': self.tokens['refresh']
        }, format='json')
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertIn('access', content)

    def test_token_refresh_failure(self):
        response = self.client.post('/accounts/token/refresh', {
            'refresh': self.tokens['access']
        }, format='json')
        self.assertEqual(response.status_code, 401)
