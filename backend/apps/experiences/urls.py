from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExperienceViewSet

app_name = 'experiences'

router = DefaultRouter()
router.register(r'', ExperienceViewSet, basename='experience')

urlpatterns = [
    path('', include(router.urls)),
]
