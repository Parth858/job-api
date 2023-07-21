from typing import Iterable, Optional
import uuid
from django.db import models

class Company(models.Model):
    
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    about=models.TextField(max_length=500)
    company_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # uuid1 uses network address for random number, so it's better to use uuid4

    def __str__(self):
        return self.name

class Job(models.Model):
    
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_role = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    description = models.TextField(default='No description provided', max_length=500)
    location = models.CharField(max_length=100)
    post_date = models.DateTimeField()
    posted = models.BooleanField(default=False)
    experience=models.IntegerField(default=0)

    def __str__(self):
        return self.job_role

class User(models.Model):

    name=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    address=models.TextField(max_length=100)
    phone=models.CharField(max_length=12)
    about=models.TextField(max_length=100)
    position=models.ForeignKey(Job, on_delete=models.CASCADE)
    resume=models.FileField(upload_to="resume/", null=True)
    profilePicture=models.ImageField(upload_to="profile_picture/", null=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, default="NA")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.resume:
            self.resume_file_path = self.resume.path
        else:
            self.resume_file_path = ""
        super().save(*args, **kwargs)