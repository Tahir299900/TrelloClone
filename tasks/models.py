from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Project(models.Model):
    name = models.CharField(max_length=200, default='Default Project')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_projects',
        null=True  # Allow null temporarily for initial migration
    )

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User, related_name='teams')
    projects = models.ManyToManyField(Project, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='leading_teams')

    def __str__(self):
        return self.name

class Task(models.Model):
    class Priority(models.TextChoices):
        HIGH = 'HIGH', 'High'
        MEDIUM = 'MEDIUM', 'Medium'
        LOW = 'LOW', 'Low'

    class Status(models.TextChoices):
        STARTED = 'STARTED', 'Started'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.STARTED
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_tasks'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Custom User Profile to extend Django's built-in User model
class UserProfile(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STANDARD = 'STANDARD', 'Standard User'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STANDARD
    )
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={'role': UserProfile.Role.STANDARD}
        )

# Register the signal
post_save.connect(create_user_profile, sender=User)
