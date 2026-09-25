from django.urls import path
from .views import UserProfileMeView

urlpatterns = [
    path('', UserProfileMeView.as_view(), name='profile_me'),
]
