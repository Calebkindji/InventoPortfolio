from rest_framework import generics, permissions
from .models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
