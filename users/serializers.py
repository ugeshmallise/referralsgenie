from .models import User
from rest_framework import serializers
from .models import JobSeekerGuestUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'mobile_number', 'email', 'password', 'resume']

    def create(self, validated_data):
        password = validated_data.pop('password')  # Remove the password from validated data
        print(password)
        user = User.objects.create(**validated_data)  # Create the user without password
        print(user)
        user.set_password(password)  # Set the password using the set_password method
        print(user)
        user.save()  # Save the user with the hashed password
        return user
    
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import JobSeekerUser

class JobSeekerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerUser
        fields = ['full_name', 'mobile_number', 'company_name', 'company_email', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')  # Remove password before saving
        jobseeker = JobSeekerUser.objects.create(**validated_data)  # Create the user without password
        jobseeker.set_password(password)  # Set the password using the set_password method
        jobseeker.save()  # Save the jobseeker with hashed password
        return jobseeker

class JobSeekerGuestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerGuestUser
        fields = ['full_name', 'user_id', 'date_joined']