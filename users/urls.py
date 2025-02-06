from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CheckInViewSet, CustomAuthToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'check-ins', CheckInViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', permission_classes([AllowAny])(CustomAuthToken.as_view()), name='auth'),
]
