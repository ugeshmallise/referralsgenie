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
    Login API for Job Seekers.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"detail": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate Job Seeker only
    user = authenticate(username=email, password=password)

    if user is None:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # Ensure the user is a Job Seeker (Prevent Job Providers from logging in)
    if not isinstance(user, User):
        return Response({"detail": "Unauthorized. Please use the correct login endpoint."}, status=status.HTTP_403_FORBIDDEN)

    # Reactivate user if needed
    if not user.is_active:
        user.is_active = True
        user.save()

    # Generate JWT tokens
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
    """
    Login API for Job Providers only.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"detail": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate user
    user = authenticate(username=email, password=password)

    # Ensure the user is a Job Provider
    if user is None or not isinstance(user, JobSeekerUser):  # Assuming User model is Job Provider
        return Response({"detail": "Unauthorized. Please use the correct login endpoint."}, status=status.HTTP_403_FORBIDDEN)

    if not user.is_active:
        user.is_active = True  # Reactivate the job provider user
        user.save()

    # Generate JWT token
    refresh = CustomRefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'message': "Job Provider login successful."
    }, status=status.HTTP_200_OK)


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


from .models import JobPosting
from .serializers import JobPostingSerializer
from rest_framework.views import APIView
class JobPostingView(APIView):
    """
    Handles all CRUD operations related to job postings.
    """

    def get_object(self, job_id):
        """ Retrieve a job posting by its UUID. """
        try:
            return JobPosting.objects.get(job_id=job_id)
        except JobPosting.DoesNotExist:
            return None

    def get(self, request, job_id=None, *args, **kwargs):
        """
        Retrieve job postings created by the specific user.
        - If job_id is provided, return that specific job.
        - Otherwise, return all job postings created by the logged-in user.
        """
        user_email = request.GET.get("email", "ugesh@gmail.com")  # Default email for now
        
        if job_id:
            job_post = self.get_object(job_id)
            if not job_post:
                return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
            if job_post.email != user_email:
                return Response({"error": "Unauthorized access to this job posting"}, status=status.HTTP_403_FORBIDDEN)
            serializer = JobPostingSerializer(job_post)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Fetch jobs posted by the logged-in user
        jobs = JobPosting.objects.filter(email=user_email)
        serializer = JobPostingSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a new job posting.
        """
        job_data = request.data.copy()
        job_data['email'] = "ugesh@gmail.com"  # Set the email automatically for now
        
        serializer = JobPostingSerializer(data=job_data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Job posted successfully",
                "job": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, job_id, *args, **kwargs):
        """
        Update a job posting.
        """
        job_post = self.get_object(job_id)
        if not job_post:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure only the owner can update the job
        user_email = request.data.get("email", "ugesh@gmail.com")  # Default email for now
        if job_post.email != user_email:
            return Response({"error": "Unauthorized access to update this job"}, status=status.HTTP_403_FORBIDDEN)

        serializer = JobPostingSerializer(job_post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Job updated successfully", "job": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, job_id, *args, **kwargs):
        """
        Delete a job posting.
        """
        job_post = self.get_object(job_id)
        if not job_post:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure only the owner can delete the job
        user_email = request.data.get("email", "ugesh@gmail.com")  # Default email for now
        if job_post.email != user_email:
            return Response({"error": "Unauthorized access to delete this job"}, status=status.HTTP_403_FORBIDDEN)

        job_post.delete()
        return Response({"message": "Job deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import JobPosting
from .serializers import JobPostingSerializer

class JobPostingListView(generics.ListAPIView):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ContactSupport
from .serializers import ContactSupportSerializer

class BaseSupportView(APIView):
    """
    A base class for handling support ticket operations.
    """

    def get_ticket(self, ticket_id):
        """Retrieve a support ticket by ticket_id"""
        try:
            return ContactSupport.objects.get(ticket_id=ticket_id)
        except ContactSupport.DoesNotExist:
            return None

    def create_ticket(self, request):
        """Create a new support ticket"""
        if request.content_type != "application/json":
            return Response({"error": "Invalid Content-Type. Use application/json"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        serializer = ContactSupportSerializer(data=request.data)
        if serializer.is_valid():
            ticket = serializer.save()  # Save the new ticket
            return Response({
                "message": "Support ticket created successfully!",
                "ticket_id": str(ticket.ticket_id)  # Ensure UUID is returned as string
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def fetch_ticket(self, ticket_id):
        """Fetch details of a specific support ticket"""
        ticket = self.get_ticket(ticket_id)
        if ticket:
            return Response({
                "ticket_id": str(ticket.ticket_id),
                "email": ticket.email,
                "is_resolved": ticket.is_resolved
            }, status=status.HTTP_200_OK)
        return Response({"error": "Support ticket not found!"}, status=status.HTTP_404_NOT_FOUND)

    def list_tickets_by_email(self, email):
        """Fetch all tickets created by a particular email"""
        tickets = ContactSupport.objects.filter(email=email)
        if tickets.exists():
            serializer = ContactSupportSerializer(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "No tickets found for this email."}, status=status.HTTP_404_NOT_FOUND)

    def resolve_ticket(self, ticket_id):
        """Mark a support ticket as resolved"""
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return Response({"error": "Support ticket not found!"}, status=status.HTTP_404_NOT_FOUND)

        if ticket.is_resolved:
            return Response({"message": "This ticket is already resolved."}, status=status.HTTP_400_BAD_REQUEST)

        ticket.is_resolved = True
        ticket.save()
        return Response({"message": "Support ticket resolved successfully!"}, status=status.HTTP_200_OK)


class ContactSupportView(BaseSupportView):
    """
    API endpoint for submitting a support issue (POST) and fetching a support ticket (GET)
    """

    def post(self, request):
        """Handles ticket creation"""
        return self.create_ticket(request)

    def get(self, request, ticket_id=None):
        """Handles fetching a specific ticket or listing all tickets for an email"""
        if ticket_id:
            return self.fetch_ticket(ticket_id)
        email = request.GET.get("email")
        if email:
            return self.list_tickets_by_email(email)
        return Response({"error": "Ticket ID or email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)


class ResolveTicketView(BaseSupportView):
    """
    API endpoint to mark a ticket as resolved (PATCH)
    """

    def patch(self, request, ticket_id):
        """Handles resolving a ticket"""
        return self.resolve_ticket(ticket_id)
