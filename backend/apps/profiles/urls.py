from django.urls import path
from .views import UserProfileMeView

app_name = 'profiles'

urlpatterns = [
    path('me/', UserProfileMeView.as_view(), name='profile_me'),
]
