from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid



# Keep your original model
class User(models.Model):
    full_name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Normal BooleanField

    def set_password(self, raw_password):
        """Hashes the password and sets it."""
        self.password = make_password(raw_password)
        
    def __str__(self):
        return self.email


class JobSeekerUser(AbstractBaseUser):
    full_name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    company_name = models.CharField(max_length=50)
    company_email = models.EmailField(unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Normal BooleanField

    def set_password(self, raw_password):
        """Hashes the password and sets it."""
        self.password = make_password(raw_password)

    def __str__(self):
        return self.email

class JobSeekerGuestUser(models.Model):
    full_name = models.CharField(max_length=50)
    user_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
