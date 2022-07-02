from random import random
from django.http import HttpResponse, JsonResponse
from .serializers import LocationQrCodeSerializer
from .models import LocationQrCode
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema, status
from drf_yasg import openapi

from rest_framework.permissions import AllowAny


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
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(
        operation_summary='read QR code information',
        operation_id='locations_get',
        tags=['locations'],
        responses={status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=LocationQrCodeSchema
                )
            }
        )},
    )
    def get(self, request):
        serializer = LocationQrCodeSerializer(LocationQrCode.objects.all(), many=True)
        return Response({'data': serializer.data}, status=200)

    @swagger_auto_schema(
        operation_summary='create QR code information',
        operation_id='random_location_create',
        tags=['locations'],
        responses={status.HTTP_201_CREATED: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'data': LocationQrCodeSchema}
        )},
    )
    def post(self, request):
        lat = (random() - 0.5) * 90
        lon = (random() - 0.5) * 180
        location_qr_code = LocationQrCode(latitude=lat, longitude=lon)
        location_qr_code.save()
        serializer = LocationQrCodeSerializer(location_qr_code)
        return Response({'data': serializer.data}, status=201)

    @swagger_auto_schema(
        operation_summary='update random QR code information',
        operation_id='random_location_update',
        tags=['locations'],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'data': LocationQrCodeSchema}
            ),
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
            return Response({'error': 'table is empty'}, status=409)
        location_qr_code = location_qr_codes[0]
        location_qr_code.latitude = (random() - 0.5) * 90
        location_qr_code.longitude = (random() - 0.5) * 180
        location_qr_code.save()
        serializer = LocationQrCodeSerializer(location_qr_code)
        return Response({'data': serializer.data}, status=200)


@swagger_auto_schema(
    method='POST',
    operation_summary='delete random QR code information',
    operation_id='random_location_delete',
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
@renderer_classes([JSONRenderer])
def test_delete(request):
    location_qr_codes = LocationQrCode.objects.order_by('?')
    if len(location_qr_codes) == 0:
        return Response({'error': 'table is empty'}, status=409)
    location_qr_code = location_qr_codes[0]
    location_qr_code.delete()
    return Response(status=204)


class LocationIdAPIView(APIView):
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(
        operation_summary='read QR code information of corresponding id',
        operation_id='location_get',
        tags=['locationId'],
        responses={
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'data': LocationQrCodeSchema}
            ),
            status.HTTP_409_CONFLICT: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='No matching object',
                    )
                }
            )
        }
    )
    def get(self, request, location_id):
        location_qr_codes = LocationQrCode.objects.filter(id=location_id)
        if len(location_qr_codes) == 0:
            return JsonResponse({'error': 'No matching object.'}, status=409)
        serializer = LocationQrCodeSerializer(location_qr_codes[0])
        return JsonResponse({'data': serializer.data}, status=200)

    @swagger_auto_schema(
        operation_summary='create QR code information of corresponding id',
        operation_id='location_create',
        tags=['locationId'],
        responses={
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'data': LocationQrCodeSchema}
            ),
            status.HTTP_409_CONFLICT: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='The id is preoccupied',
                    )
                }
            )
        }
    )
    def post(self, request, location_id):
        presence = LocationQrCode.objects.filter(id=location_id)
        if len(presence) != 0:
            return JsonResponse({'error': 'The id is preoccupied'}, status=409)
        lat = (random() - 0.5) * 90
        lon = (random() - 0.5) * 180
        location_qr_code = LocationQrCode(latitude=lat, longitude=lon, id=location_id)
        location_qr_code.save()
        serializer = LocationQrCodeSerializer(location_qr_code)
        return JsonResponse({'data': serializer.data}, status=201)

    @swagger_auto_schema(
        operation_summary='update QR code information of corresponding id',
        operation_id='location_update',
        tags=['locationId'],
        responses={
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'data': LocationQrCodeSchema}
            ),
            status.HTTP_409_CONFLICT: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='No matching object',
                    )
                }
            )
        }
    )
    def patch(self, request, location_id):
        location_qr_codes = LocationQrCode.objects.filter(id=location_id)
        if len(location_qr_codes) == 0:
            return JsonResponse({'error': 'No matching object'}, status=409)
        location_qr_code = location_qr_codes.first()
        location_qr_code.latitude = ( random() - 0.5 ) * 90
        location_qr_code.longitude = ( random() - 0.5 ) * 180
        location_qr_code.save()
        serializer = LocationQrCodeSerializer(location_qr_code)
        return JsonResponse({'data': serializer.data})

    @swagger_auto_schema(
        operation_summary='delete QR code information of corresponding id',
        operation_id='location_delete',
        tags=['locationId'],
        responses={
            status.HTTP_204_NO_CONTENT: '',
            status.HTTP_409_CONFLICT: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='No matching object',
                    )
                }
            )
        }
    )
    def delete(self, request, location_id):
        location_qr_codes = LocationQrCode.objects.filter(id=location_id)
        if len(location_qr_codes) == 0:
            return JsonResponse({'error': 'No matching object'}, status=409)
        location_qr_code = location_qr_codes.first()
        location_qr_code.delete()
        return HttpResponse(status=204)
