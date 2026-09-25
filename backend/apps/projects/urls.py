from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectMediaViewSet, ProjectSkillViewSet, ExternalLinkViewSet

app_name = 'projects'

router = DefaultRouter()
router.register(r'media', ProjectMediaViewSet, basename='project-media')
router.register(r'skills', ProjectSkillViewSet, basename='project-skill')
router.register(r'links', ExternalLinkViewSet, basename='external-link')
router.register(r'', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]
