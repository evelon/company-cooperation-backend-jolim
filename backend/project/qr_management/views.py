from random import choice, random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import LocationQrCode
from .serializers import LocationQrCodeSerializer
from rest_framework.views import APIView

class LocationAPIView(APIView):
    def get(self, request):
        serializer = LocationQrCodeSerializer(LocationQrCode.objects.all(), many=True)
        return JsonResponse({'data': serializer.data}, status=200)

class LocationIdAPIView(APIView):
    def get(self, request, location_id):
        location_qr_codes = LocationQrCode.objects.filter(id=location_id)
        if len(location_qr_codes) == 0:
            return JsonResponse({'error': 'No matching object.'}, status=409)
        serializer = LocationQrCodeSerializer(location_qr_codes[0])
        return JsonResponse({'data': serializer.data}, status=200)

    def post(self, request, location_id):
        presence = LocationQrCode.objects.filter(id=location_id)
        if len(presence) != 0:
            return JsonResponse({'error': 'The id is preoccupied'}, status=409)
        lat = ( random() - 0.5 ) * 90
        lon = ( random() - 0.5 ) * 180
        location_qr_code = LocationQrCode(latitude=lat, longitude=lon, id=location_id)
        location_qr_code.save()
        serializer = LocationQrCodeSerializer(location_qr_code)
        return JsonResponse({'data': serializer.data}, status=201)

    def patch(self, request, location_id):
        location_qr_codes = LocationQrCode.objects.filter(id=location_id)
        if len(location_qr_codes) == 0:
            return JsonResponse({'error': 'No matching object.'}, status=409)
        location_qr_code = location_qr_codes.first()
        location_qr_code.latitude = ( random() - 0.5 ) * 90
        location_qr_code.longitude = ( random() - 0.5 ) * 180
        location_qr_code.save()
        serializer = LocationQrCodeSerializer(location_qr_code)
        return JsonResponse({'data': serializer.data})

    def delete(self, request, location_id):
        location_qr_codes = LocationQrCode.objects.filter(id=location_id)
        if len(location_qr_codes) == 0:
            return JsonResponse({'error': 'No matching object.'}, status=409)
        location_qr_code = location_qr_codes.first()
        location_qr_code.delete()
        return HttpResponse(status=204)
