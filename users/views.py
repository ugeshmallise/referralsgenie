from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .auth import CustomRefreshToken
from .serializers import UserSerializer, JobSeekerUserSerializer,JobSeekerGuestUser
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


# Register User
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully!",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login User
from django.contrib.auth import authenticate, get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import JobSeekerUser  # Import JobSeekerUser if it's a separate model
from users.tokens import RefreshToken # Import your token generator

User = get_user_model()  # Get the User model dynamically

@api_view(['POST'])
def login_user(request):
    """
    Login API with authentication.
    It verifies the email and password using Django's authentication system,
    activates the user, and returns new tokens.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"detail": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Try authenticating using Django's built-in authentication
    user = authenticate(username=email, password=password)

    if user is None:
        # If not found in User model, check JobSeekerUser model
        try:
            user = JobSeekerUser.objects.get(email=email)
        except JobSeekerUser.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Verify password manually (only if JobSeekerUser model does not use Django authentication)
        if hasattr(user, 'check_password') and not user.check_password(password):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # Reactivate user if needed
    if not user.is_active:
        user.is_active = True
        user.save()

    # Generate new tokens
    refresh = CustomRefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'message': "Login successful."
    }, status=status.HTTP_200_OK)



# Register Job Seeker
@api_view(['POST'])
def register_jobprovider(request):
    if request.method == 'POST':
        serializer = JobSeekerUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Job Seeker registered successfully!",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login Job Seeker
@api_view(['POST'])
def login_jobprovider(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"detail": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=email, password=password)

    if user is not None:
        if not user.is_active:
            user.is_active = True  # Reactivate the job seeker user
            user.save()

        # Generate new tokens
        refresh = CustomRefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': "Login successful and account reactivated." if not user.is_active else "Login successful."
        }, status=status.HTTP_200_OK)

    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .auth import CustomRefreshToken
from .serializers import UserSerializer, JobSeekerUserSerializer
from .models import User, JobSeekerUser  # Import your models
from rest_framework_simplejwt.tokens import RefreshToken

# Logout User
@api_view(['POST'])
def logout_user(request):
    """
    Logs out the user by setting is_active to False and blacklisting tokens.
    Expects 'email' in request data.
    """
    email = request.data.get('email')

    if not email:
        return Response({"detail": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Try to find user in both tables
    user = None
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        try:
            user = JobSeekerUser.objects.get(email=email)
        except JobSeekerUser.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Set is_active to False
    user.is_active = False
    user.save()

    # Blacklist refresh token (if provided)
    refresh_token = request.data.get('refresh')
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            pass  # Ignore errors if token is already invalid

    return Response({
        "message": "User logged out successfully. Account has been deactivated."
    }, status=status.HTTP_200_OK)


from datetime import timedelta
from django.utils.timezone import now
import jwt
from django.conf import settings

@api_view(['POST'])
def jobseeker_guest_login(request):
    """
    Creates a guest job seeker account with a full name only and returns a manually generated JWT token.
    """
    full_name = request.data.get('full_name')
    
    if not full_name:
        return Response({"detail": "Full name is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    guest_user = JobSeekerGuestUser.objects.create(full_name=full_name)

    # Manually create JWT payload
    payload = {
        'user_id': str(guest_user.user_id),
        'full_name': guest_user.full_name,
        'exp': now() + timedelta(days=1)  # Token expires in 1 day
    }

    # Encode JWT token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return Response({
        'access_token': token,
        'user_id': str(guest_user.user_id),
        'message': 'Logged in as guest job seeker successfully.'
    }, status=status.HTTP_200_OK)

# Guest Logout for Job Seekers
@api_view(['POST'])
def jobseeker_guest_logout(request):
    """
    Permanently deletes the guest job seeker user from the database upon logout.
    """
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response({"detail": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        guest_user = JobSeekerGuestUser.objects.get(user_id=user_id)
        guest_user.delete()
        return Response({"message": "Guest user logged out and deleted successfully."}, status=status.HTTP_200_OK)
    except JobSeekerGuestUser.DoesNotExist:
        return Response({"detail": "Guest user not found"}, status=status.HTTP_404_NOT_FOUND)
