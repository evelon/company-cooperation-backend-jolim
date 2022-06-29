from random import choice, random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .serializer import LocationQrCodeSerializer
from .models import LocationQrCode
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema, status
from drf_yasg import openapi


LocationQrCodeSchema = openapi.Schema(
    'qr-code',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
        'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
        'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
        'validity': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'owner': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_INT32)
    }
)

class LocationAPIView(APIView):

    @swagger_auto_schema(
        operation_summary='read QR code information',
        operation_id='getLocations',
        tags=['locations'],
        responses={status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=LocationQrCodeSchema
                )
            }
        )}
    )
    def get(self, request):
        serializer = LocationQrCodeSerializer(LocationQrCode.objects.all(), many=True)
        return JsonResponse({'data': serializer.data}, status=200)

    @swagger_auto_schema(
        operation_summary='create QR code information',
        operation_id='createLocation',
        tags=['locations'],
        responses={status.HTTP_201_CREATED: LocationQrCodeSchema}
    )
    def post(self, request):
        lat = ( random() - 0.5 ) * 90
        lon = ( random() - 0.5 ) * 180
        location_qr_code = LocationQrCode(latitude=lat, longitude=lon)
        location_qr_code.save()
        serializer = LocationQrCodeSerializer(location_qr_code)
        return JsonResponse({'data': serializer.data}, status=201)

    @swagger_auto_schema(
        operation_summary='update random QR code information',
        operation_id='updateLocation',
        tags=['locations'],
        responses={
            status.HTTP_200_OK: LocationQrCodeSchema,
            status.HTTP_409_CONFLICT: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='table is empty',
                    )
                }
            )
        }
    )
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

@swagger_auto_schema(
    method='POST',
    operation_summary='delete random QR code information',
    operation_id='deleteLocation',
    tags=['locations'],
    responses={
        status.HTTP_204_NO_CONTENT: '',
        status.HTTP_409_CONFLICT: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'error': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example='table is empty',
                )
            }
        )
    }
)
@api_view(['POST'])
def test_delete(request):
    location_qr_codes = LocationQrCode.objects.order_by('?')
    if len(location_qr_codes) == 0:
        return JsonResponse({'error': 'table is empty'}, status=409)
    location_qr_code = location_qr_codes[0]
    location_qr_code.delete()
    return HttpResponse(status=204)