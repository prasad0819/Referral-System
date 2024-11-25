from .models import UserProfile
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from referral_system.api.serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
