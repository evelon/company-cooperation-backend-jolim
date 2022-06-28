from random import choice, random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .serializer import LocationQrCodeSerializer
from .models import LocationQrCode
from rest_framework.views import APIView
from rest_framework.decorators import api_view


class LocationAPIView(APIView):
    def get(self, request):
        serializer = LocationQrCodeSerializer(LocationQrCode.objects.all(), many=True)
        return JsonResponse({'data': serializer.data}, status=200)

    def post(self, request):
        lat = ( random() - 0.5 ) * 90
        lon = ( random() - 0.5 ) * 180
        location_qr_code = LocationQrCode(latitude=lat, longitude=lon)
        location_qr_code.save()
        serializer = LocationQrCodeSerializer(location_qr_code)
        return JsonResponse({'data': serializer.data}, status=201)

    def patch(self, request):
        location_qr_codes = LocationQrCode.objects.order_by('?')
        if len(location_qr_codes) == 0:
            return JsonResponse({'error': 'table is empty'}, status=409)
        location_qr_code = location_qr_codes[0]
        location_qr_code.latitude = ( random() - 0.5 ) * 90
        location_qr_code.longitude = ( random() - 0.5 ) * 180
        location_qr_code.save()
        serializer = LocationQrCodeSerializer(location_qr_code)
        return JsonResponse({'data': serializer.data}, status=200)

@api_view(['POST'])
def test_delete(request):
    location_qr_codes = LocationQrCode.objects.order_by('?')
    if len(location_qr_codes) == 0:
        return JsonResponse({'error': 'table is empty'}, status=409)
    location_qr_code = location_qr_codes[0]
    location_qr_code.delete()
    return HttpResponse(status=204)