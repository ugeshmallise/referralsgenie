from django.contrib.auth.hashers import check_password
from .models import User

class EmailBackend:
    """
    Custom authentication backend that works with our User model
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if check_password(password, user.password):
                # Add these properties for JWT compatibility
                user.is_authenticated = True
                user.username = user.email  # Add username property (but don't store in DB)
                return user
            return None
        except User.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.is_authenticated = True
            user.username = user.email  # Add username property (but don't store in DB)
            return user
        except User.DoesNotExist:
            return None
        

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import JobSeekerUser

class EmailBackendtest(BaseBackend):
    """
    Custom authentication backend for JobSeekerUser that uses email as the username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Find the user by email (email is treated as username)
            user = JobSeekerUser.objects.get(email=username)
            if check_password(password, user.password):
                return user
            return None
        except JobSeekerUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return JobSeekerUser.objects.get(pk=user_id)
        except JobSeekerUser.DoesNotExist:
            return None
