from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Location
import json
from rest_framework_simplejwt.tokens import RefreshToken


def get_access_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class TestLocationsView(TestCase):

    def setUp(self):
        self.client = APIClient()
        Location.objects.create(latitude=33.3, longitude=66.6)
        get_user_model().objects.create_user(
            username='username',
            password='password',
            email='email@example.com',
            is_active=True,
            verified=True,
        )
        user = get_user_model().objects.get(username='username')
        self.token = get_access_tokens_for_user(user)
        self.client.force_authenticate(user=user)

    def qr_code_content_validator(self, content):
        self.assertIn('id', content)
        self.assertIn('latitude', content)
        self.assertIn('longitude', content)
        self.assertIn('validity', content)
        self.assertIn('owner', content)

    def test_get(self):
        response = self.client.get('/qr-code/locations/random')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        if len(data) >= 1:
            self.qr_code_content_validator(data[0])

    def test_post(self):
        new_client = APIClient()
        auth_headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.token}',
        }
        response = new_client.post('/qr-code/locations/random', **auth_headers)

        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.qr_code_content_validator(content)
        location_qr_codes = Location.objects.all()
        self.assertEqual(len(location_qr_codes), 2)

    def test_patch(self):
        response = self.client.patch('/qr-code/locations/random')

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.qr_code_content_validator(content)
        location_qr_codes = Location.objects.all()
        self.assertEqual(len(location_qr_codes), 1)

    def test_random_delete(self):
        response = self.client.post('/qr-code/locations/random-delete')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')
        location_qr_codes = Location.objects.all()
        self.assertEqual(len(location_qr_codes), 0)

