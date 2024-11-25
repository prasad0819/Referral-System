from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from shortuuid.django_fields import ShortUUIDField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)

    # Adding the below to maintain parity with AbstractUser
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    phone = PhoneNumberField()
    city = models.CharField(max_length=50)
    referral_code = ShortUUIDField(length=10)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referees')
    created_at = models.DateTimeField(auto_now_add=True)


class Dummy(models.Model):
    pass

