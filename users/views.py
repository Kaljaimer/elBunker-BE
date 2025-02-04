from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .models import CustomUser, UserLogin
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # For development, change this for production

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={201: UserSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Log in a user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: 'Login successful', 401: 'Invalid credentials'}
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            UserLogin.objects.create(user=user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
