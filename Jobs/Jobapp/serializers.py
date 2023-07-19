from rest_framework import serializers
from .models import Company, Job, UserProfile

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'company', 'title', 'description')

class CompanySerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'location', 'jobs')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'job', 'username', 'email', 'bio', 'resume')
