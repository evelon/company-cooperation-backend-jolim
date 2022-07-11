from django.utils.decorators import method_decorator
from .serializers import LocationSerializer
from .models import Location
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from qr_management.serializers import RandomLocationSerializer
from drf_yasg.utils import swagger_auto_schema, status
from drf_yasg import openapi


LocationQrCodeSchema = openapi.Schema(
    'qr-code',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_UUID
        ),
        'latitude': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            format=openapi.FORMAT_FLOAT,
            example=33.1424342
        ),
        'longitude': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            format=openapi.FORMAT_FLOAT,
            example=63.2423175
        ),
        'validity': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            example=True
        ),
        'owner': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            format=openapi.FORMAT_INT32,
            example=3
        )
    }
)


class OwnerCreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.auth['user_id']
        return super().create(request, *args, **kwargs)


class OwnerUpdateModelMixin(mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.owner != request.auth['user_id']:
            return Response({'detail': 'The user is not the owner'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class RandomLocationAPIView(
    OwnerCreateModelMixin,
    generics.GenericAPIView,
    mixins.ListModelMixin,
):
    queryset = Location.objects.all()
    serializer_class = RandomLocationSerializer

    @swagger_auto_schema(
        operation_summary='read QR code information',
        operation_id='locations_get',
        tags=['locations'],
    )
    def get(self, request, *args, **kwargs):
        return self.list(self. request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='create random QR code information',
        operation_id='random_location_create',
        tags=['locations'],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

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
    def patch(self, request, *args, **kwargs):
        location_qr_codes = Location.objects.order_by('?')
        if len(location_qr_codes) == 0:
            return Response({'error': 'table is empty'}, status=409)
        serializer = self.get_serializer(location_qr_codes[0])
        serializer.update(location_qr_codes[0], None)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RandomLocationDeleteAPIView(APIView):
    @swagger_auto_schema(
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
    def post(self, request, *args, **kwargs):
        location_qr_codes = Location.objects.order_by('?')
        if len(location_qr_codes) == 0:
            return Response({'error': 'table is empty'}, status=409)
        location_qr_code = location_qr_codes[0]
        location_qr_code.delete()
        return Response(status=204)


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='read QR code information of corresponding id',
    operation_id='location_get',
    tags=['locationId'],
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='create QR code information of corresponding id',
    operation_id='location_create',
    tags=['locationId'],
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='update QR code information of corresponding id',
    operation_id='location_update',
    tags=['locationId'],
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='delete QR code information of corresponding id',
    operation_id='location_delete',
    tags=['locationId'],
))
class LocationViewSet(
    OwnerCreateModelMixin,
    OwnerUpdateModelMixin,
    viewsets.ModelViewSet
):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
