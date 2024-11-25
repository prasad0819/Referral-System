from .models import CustomUser
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from referral_system.api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
