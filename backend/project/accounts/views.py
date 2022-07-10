from rest_framework import generics
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from .serializers import RegistrationSerializer
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from config import settings
from urllib.parse import urlencode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='create an user account',
    operation_id='account_create',
    tags=['accounts'],
    responses={
        status.HTTP_201_CREATED: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="3",
                ),
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    maxLength=24,
                    minLength=4,
                    example="username",
                ),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="email@example.com",
                )
            },
            required=['id', 'username', 'email']
        )
    }
))
class CreateUserAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        try:
            user = get_user_model().objects.get(id=response.data["id"])
        except ObjectDoesNotExist:
            return Response(data={"error": "Failed to create a user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        token = default_token_generator.make_token(user)
        verification_url = settings.SERVERNAME + '/accounts/verify?' + urlencode({'user': user.id, 'token': token})
        email = EmailMessage('Test Email Verification', verification_url, to=[user.email])
        email.send()
        return response


class ResendVerificationAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Resend verification email of <username>',
        operation_id='verification_resend',
        manual_parameters=[openapi.Parameter(
            'username',
            'IN_QUERY',
            'username to send email',
            required=True,
            type=openapi.TYPE_STRING
        )],
        responses={
            status.HTTP_204_NO_CONTENT: '',
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='no username provided in query'
                    )
                },
                required=['error']
            ),
            status.HTTP_409_CONFLICT: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='User has already verified email',
                    )
                },
                required=['error']
            )
        }
    )
    def post(self, request, **kwargs):
        if 'username' not in request.GET:
            return Response({'error': 'no username provided in query'}, status=status.HTTP_400_BAD_REQUEST)
        username = request.GET['username']
        try:
            user = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist:
            return Response({'error': 'No such username'}, status=status.HTTP_400_BAD_REQUEST)
        if user.verified is True:
            return Response({'error': 'User has already verified email'}, status=status.HTTP_409_CONFLICT)
        token = default_token_generator.make_token(user)
        verification_url = settings.SERVERNAME + '/accounts/verify?' + urlencode({'user': user.id, 'token': token})
        email = EmailMessage('Test Email Verification', verification_url, to=[user.email])
        email.send()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VerifyEmailAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Verify email link',
        operation_id='email_verify',
        manual_parameters=[
            openapi.Parameter(
                'user',
                'IN_QUERY',
                'user id',
                required=True,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'token',
                'IN_QUERY',
                'token for email verification',
                required=True,
                type=openapi.TYPE_STRING,
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'msg': openapi.Schema(type=openapi.TYPE_STRING, example='Verification successful'),
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="No 'user' or 'token' in query"
                    )
                },
                required=['error']
            ),
            status.HTTP_409_CONFLICT: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='User is already verified'
                    )
                },
                required=['error']
            ),
        }
    )
    def get(self, request, **kwargs):
        if 'user' not in request.GET or 'token' not in request.GET:
            return Response({'error': "No 'user' or 'token' in query"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = int(request.GET['user'])
        except ValueError:
            return Response({'error': 'user id is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        token = request.GET['token']
        try:
            user = get_user_model().objects.get(id=user)
        except ObjectDoesNotExist:
            return Response({'error': 'No such user'}, status=400)
        check = default_token_generator.check_token(user, token)
        if check is False:
            return Response({'error': 'Token check failed'}, status=400)
        if user.verified is True:
            return Response({'error': 'User is already verified'}, status=409)
        user.verified = True
        user.is_active = True
        user.save()
        return Response({'msg': 'Verification successful'})


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "username": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="This field is required.",
                    ),
                    "password": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="This field is required.",
                    )
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='This field is required.',
                        )
                    )
                }
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='Token is invalid or expired',
                    ),
                    'code': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='token_not_valid',
                    )
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='This field is required.',
                        )
                    )
                }
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='Token is invalid or expired',
                    ),
                    'code': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='token_not_valid',
                    )
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
