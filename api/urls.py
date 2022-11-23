from django.conf import settings
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register('profiles', ProfileViewSet)
router.register('projects', ProjectViewSet)
router.register('messages', MessageViewSet)
router.register('reviews', ReviewViewSet)
router.register('skills', SkillsViewSet)
router.register('tags', TagViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]