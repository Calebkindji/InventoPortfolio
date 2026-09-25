from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SkillCategoryViewSet, SkillViewSet, ProfileSkillViewSet

app_name = 'skills'

router = DefaultRouter()
router.register(r'categories', SkillCategoryViewSet, basename='skill-category')
router.register(r'catalog', SkillViewSet, basename='skill')
router.register(r'profile', ProfileSkillViewSet, basename='profile-skill')

urlpatterns = [
    path('', include(router.urls)),
]
