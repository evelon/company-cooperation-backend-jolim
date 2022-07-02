from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from django.contrib.auth import get_user_model
from .models import LocationQrCode
from .views import LocationAPIView, test_delete
import json


class TestLocationsView(TestCase):

    def setUp(self):
        self.client = APIClient()
        LocationQrCode.objects.create(latitude=33.3, longitude=66.6)
        get_user_model().objects.create_user(
            username='username',
            password='password',
            email='email@example.com'
        )
        user = get_user_model().objects.get(username='username')
        self.client.force_authenticate(user=user)

    def test_get(self):
        response = self.client.get('/qr-code/locations')

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)

        self.assertIn('data', content)
        if 'data' in content:
            data = content['data']
            self.assertGreaterEqual(len(data), 1)
            if len(data) >= 1:
                self.assertIn('id', data[0])
                self.assertIn('latitude', data[0])
                self.assertIn('longitude', data[0])
                self.assertIn('validity', data[0])
                self.assertIn('owner', data[0])

    def test_post(self):
        response = self.client.post('/qr-code/locations')

        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertIn('data', content)
        self.qr_code_content_validator(content)
        location_qr_codes = LocationQrCode.objects.all()
        self.assertEqual(len(location_qr_codes), 2)

    def qr_code_content_validator(self, content):
        if 'data' in content:
            data = content['data']
            self.assertIn('id', data)
            self.assertIn('latitude', data)
            self.assertIn('longitude', data)
            self.assertIn('validity', data)
            self.assertIn('owner', data)

    def test_patch(self):
        response = self.client.patch('/qr-code/locations')

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('data', content)
        self.qr_code_content_validator(content)
        location_qr_codes = LocationQrCode.objects.all()
        self.assertEqual(len(location_qr_codes), 1)

    def test_random_delete(self):
        response = self.client.post('/qr-code/locations/random-delete')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')
        location_qr_codes = LocationQrCode.objects.all()
        self.assertEqual(len(location_qr_codes), 0)
