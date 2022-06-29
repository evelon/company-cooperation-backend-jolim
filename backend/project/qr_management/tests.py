from django.test import TestCase
from rest_framework.test import APIClient
from .models import LocationQrCode
import json


class TestLocationsViews(TestCase):
    client = APIClient()

    def setUp(self):
        LocationQrCode.objects.create(latitude=33.3, longitude=66.6)

    def test_get(self):
        response = TestLocationsViews.client.get('/locations')
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
        response = TestLocationsViews.client.post('/locations')
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertIn('data', content)
        if 'data' in content:
            data = content['data']
            self.assertIn('id', data)
            self.assertIn('latitude', data)
            self.assertIn('longitude', data)
            self.assertIn('validity', data)
            self.assertIn('owner', data)
        location_qr_codes = LocationQrCode.objects.all()
        self.assertEqual(len(location_qr_codes), 2)

    def test_patch(self):
        response = TestLocationsViews.client.patch('/locations')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('data', content)
        if 'data' in content:
            data = content['data']
            self.assertIn('id', data)
            self.assertIn('latitude', data)
            self.assertIn('longitude', data)
            self.assertIn('validity', data)
            self.assertIn('owner', data)
        location_qr_codes = LocationQrCode.objects.all()
        self.assertEqual(len(location_qr_codes), 1)

    def test_random_delete(self):
        response = TestLocationsViews.client.post('/locations/random-delete')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')
        location_qr_codes = LocationQrCode.objects.all()
        self.assertEqual(len(location_qr_codes), 0)
