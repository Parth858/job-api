from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    description = models.TextField(default='No description provided')

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    def default_resume():
        return 'default_resume.pdf'
    
    username = models.CharField(max_length=255)
    email = models.EmailField()
    bio = models.TextField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants', null=True)
    resume = models.FileField(upload_to='resumes/',default=default_resume)

    def __str__(self):
        return self.username
