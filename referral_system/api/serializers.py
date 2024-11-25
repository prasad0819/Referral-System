from .models import CustomUser, UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    referrer_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        exclude = ['user']
        read_only_fields = ['created_at', 'referral_code', 'referred_by']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = CustomUser.objects.create(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user



