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


class JobPosting(models.Model):
    job_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    company_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    experience_required = models.CharField(max_length=50)
    job_description = models.TextField()
    official_link = models.URLField()
    email = models.EmailField(default="ugesh@gmail.com")  # Ensure this line is present
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} at {self.company_name}"


import uuid
from django.db import models

class ContactSupport(models.Model):
    ticket_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Unique ticket ID
    name = models.CharField(max_length=100)  # User's name
    email = models.EmailField()  # User's email
    issue_description = models.TextField()  # Detailed issue description
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of ticket creation
    is_resolved = models.BooleanField(default=False)  # Default unresolved status

    def __str__(self):
        return f"Support Ticket {self.ticket_id} - {self.name}"
