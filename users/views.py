from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import CustomUser, CheckIn
from .serializers import UserSerializer, CheckInSerializer
from .models import ExpiringToken

class CustomAuthToken(ObtainAuthToken):
    @swagger_auto_schema(
        operation_description="Authenticate user and return token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['username', 'password']
        ),
        responses={200: 'Authentication successful', 400: 'Invalid credentials'}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = ExpiringToken.objects.get_or_create(user=user)

            if not created and token.is_expired():
                token.delete()
                token = ExpiringToken.objects.create(user=user)

            return Response({
                'token': token.key,
                'expires': token.expires,
                'user_id': user.pk,
                'email': user.email,
                'name': user.name,
                'lastname': user.lastname,
                'is_superuser': user.is_superuser
            })
        except exceptions.ValidationError as e:
            return Response({
                'error': 'Authentication failed',
                'detail': 'Usuario o contraseña incorrectos'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'error': 'Ha ocurrido un error inesperado',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'lastname': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'email', 'password', 'name', 'lastname']
        ),
        responses={201: UserSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class CheckInViewSet(viewsets.ModelViewSet):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new check-in for the authenticated user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID')
            },
            required=['user_id']
        ),
        responses={201: CheckInSerializer()}
    )
    def create(self, request):
        user_id = request.data.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        check_in = CheckIn.objects.create(user=user)
        serializer = self.get_serializer(check_in)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Get all check-ins",
        responses={200: CheckInSerializer(many=True)}
    )
    def list(self, request):
        check_ins = CheckIn.objects.all().order_by('-check_in_time')
        serializer = self.get_serializer(check_ins, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get the last check-in of a user",
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description="ID of the user",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: CheckInSerializer,
            404: 'User not found or no check-ins available'
        }
    )
    @action(detail=False, methods=['get'])
    def last_checkin(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, id=user_id)
        last_checkin = CheckIn.objects.filter(user=user).order_by('-check_in_time').first()

        if not last_checkin:
            return Response({"message": "No check-ins found for this user"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(last_checkin)
        return Response(serializer.data)



    @swagger_auto_schema(
        operation_description="Get all check-ins for a specific user",
        responses={200: CheckInSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def user_check_ins(self, request):
        user_id = request.query_params.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        check_ins = CheckIn.objects.filter(user=user).order_by('-check_in_time')
        serializer = self.get_serializer(check_ins, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Delete a specific check-in",
        responses={204: "No content"}
    )
    def destroy(self, request, pk=None):
        check_in = get_object_or_404(CheckIn, pk=pk)
        check_in.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
