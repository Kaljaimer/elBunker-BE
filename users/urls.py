from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CheckInViewSet, CustomAuthToken

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'check-ins', CheckInViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', CustomAuthToken.as_view(), name='auth'),
]
