from rest_framework_simplejwt.tokens import Token
from datetime import datetime, timedelta
from django.conf import settings
import uuid

class CustomToken(Token):
    """Custom JWT token implementation that doesn't rely on Django's User model"""
    token_type = 'access'
    lifetime = timedelta(minutes=5)
    
    @classmethod
    def for_user(cls, user):
        """
        Returns an authorization token for the given user that will be provided
        after authenticating the user's credentials.
        """
        token = cls()
        token.payload = {
            'token_type': token.token_type,
            'exp': datetime.utcnow() + token.lifetime,
            'iat': datetime.utcnow(),
            'jti': uuid.uuid4().hex,
            'user_id': user.id,
            'email': user.email,
        }
        return token

class CustomRefreshToken(CustomToken):
    """Custom refresh token implementation"""
    token_type = 'refresh'
    lifetime = timedelta(days=1)
    
    @property
    def access_token(self):
        """Get an access token based on this refresh token"""
        access = CustomToken()
        access.payload = self.payload.copy()
        access.payload['token_type'] = 'access'
        access.payload['exp'] = datetime.utcnow() + CustomToken.lifetime
        return access