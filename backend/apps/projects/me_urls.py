from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectMediaViewSet, ProjectSkillViewSet, ExternalLinkViewSet

project_router = DefaultRouter()
project_router.register(r'', ProjectViewSet, basename='me-project')
media_router = DefaultRouter()
media_router.register(r'', ProjectMediaViewSet, basename='project-media')
skill_router = DefaultRouter()
skill_router.register(r'', ProjectSkillViewSet, basename='project-skill')
link_router = DefaultRouter()
link_router.register(r'', ExternalLinkViewSet, basename='external-link')

urlpatterns = [
    path('', include(project_router.urls)),
    path('<int:project_pk>/media/', include(media_router.urls)),
    path('<int:project_pk>/skills/', include(skill_router.urls)),
    path('<int:project_pk>/links/', include(link_router.urls)),
]
