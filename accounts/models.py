from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.email


class Profile(models.Model):

    GENDER_CHOICES = [
        ('male', 'مرد'),
        ('female', 'زن'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - Profile"