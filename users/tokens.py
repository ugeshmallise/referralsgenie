# users/tokens.py
from rest_framework_simplejwt.tokens import RefreshToken as OriginalRefreshToken
from django.conf import settings

class RefreshToken(OriginalRefreshToken):
    @classmethod
    def for_user(cls, user):
        """
        Override this method to work with our custom User model
        """
        token = cls()
        token['user_id'] = user.pk
        token['email'] = user.email
        
        return token