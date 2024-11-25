from django.db import transaction

from .models import CustomUser, UserProfile
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserProfileSerializer(serializers.ModelSerializer):
    referrer_code = serializers.CharField(write_only=True, required=False, allow_blank=True)
    user = CustomUserSerializer()

    class Meta:
        model = UserProfile
        exclude = []
        read_only_fields = ['created_at', 'referral_code', 'referred_by']

    def validate_referrer_code(self, value):
        if value:
            if not UserProfile.objects.filter(referral_code=value).exists():
                raise serializers.ValidationError("The referral code is invalid.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        referrer_code = validated_data.pop('referrer_code', None)
        user_data = validated_data.pop('user')

        user_serializer = CustomUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        if referrer_code:
            referrer = UserProfile.objects.get(referral_code=referrer_code)
            validated_data['referred_by'] = referrer

        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile
