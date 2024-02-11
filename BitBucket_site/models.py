import django
from django.db import models
#from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
from django.conf import settings
#from BitBucket_site.models import User
from django.contrib.auth.models import AbstractUser
#from .models import User  # Make sure the path is correct based on your project structure

#from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Add any additional fields you want for your user model
    # Example:
    bio = models.TextField(blank=True)
    id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    password =models.CharField(max_length=128, verbose_name='password')
    last_login= models.DateTimeField(blank=True, null=True, verbose_name='last login')
    is_superuser=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')     
    username= models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')
    first_name= models.CharField(blank=True, max_length=150, verbose_name='first name')
    last_name= models.CharField(blank=True, max_length=150, verbose_name='last name')
    email= models.EmailField(blank=True, max_length=254, verbose_name='email address')
    is_staff=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')
    is_active= models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')
    date_joined= models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')
    bio= models.TextField(blank=True)
    groups= models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')
    user_permissions= models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')

    def __str__(self):
        return self.username

class Repository(models.Model):
    name = models.CharField(max_length=100)
    repo_slug = models.SlugField(unique=True)
    repo_data = models.JSONField(null=True)

    def __str__(self):
        return self.repo_slug

class Manager(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    
class AccessRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
    )

    user = models.ForeignKey('BitBucket_site.User', on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=50)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)  # ForeignKey to Manager model
    timestamp = models.DateTimeField(auto_now_add=True)
    User_display_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    approval_url = models.URLField(blank=True, null=True)  # URL for manager to approve

    def __str__(self):
        return f"Access request for {self.repository.name} by {self.user.username}"

class ApprovalRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
    )

    requester = models.ForeignKey('BitBucket_site.User', on_delete=models.CASCADE, related_name='approval_requests')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='approvals')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    reason_for_approval = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request from {self.requester.username} to {self.manager.username}"

