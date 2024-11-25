from django.db import transaction

from .models import CustomUser, UserProfile
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserProfileSerializer(serializers.ModelSerializer):
    # The code entered during user registration which must match an existing user's referral code
    referrer_code = serializers.CharField(write_only=True, required=False, allow_blank=True)
    user = CustomUserSerializer()

    class Meta:
        model = UserProfile
        exclude = []
        read_only_fields = ['created_at', 'referral_code', 'referred_by']

    # Ensures that the referral code entered during user registration is valid.
    def validate_referrer_code(self, value):
        if value:
            if not UserProfile.objects.filter(referral_code=value).exists():
                raise serializers.ValidationError("The referral code is invalid.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        # User creation
        user_data = validated_data.pop('user')
        user_serializer = CustomUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Use `referrer_code` to set `referred_by`
        referrer_code = validated_data.pop('referrer_code', None)
        if referrer_code:
            referrer = UserProfile.objects.get(referral_code=referrer_code)
            validated_data['referred_by'] = referrer

        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile


# To view list of users that a user has referred.
class RefereeSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'created_at']


# Adding User ID, Email fields to Token response
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['id'] = self.user.id
        data['email'] = self.user.email

        return data
