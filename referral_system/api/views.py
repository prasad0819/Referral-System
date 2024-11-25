from rest_framework.decorators import action
from rest_framework.response import Response

from .models import UserProfile
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from referral_system.api.serializers import UserProfileSerializer, RefereeSerializer, CustomTokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenObtainPairView


class UserProfileViewSet(viewsets.ModelViewSet):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    # Allow public access to `create` for user registration
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    # List of users that registered using current user's referral code
    @action(detail=True, methods=['get'])
    def referees(self, request, pk=None):
        try:
            user_profile = self.get_object()
            referees = user_profile.referees.all()
            serialized_referees = RefereeSerializer(referees, many=True, context={'request': request})
            return Response(serialized_referees.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User Profile not found.'}, status=404)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

