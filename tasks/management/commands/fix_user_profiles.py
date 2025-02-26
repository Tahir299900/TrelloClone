from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tasks.models import UserProfile

class Command(BaseCommand):
    help = 'Ensures all users have a UserProfile with correct role'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'role': UserProfile.Role.ADMIN if user.is_superuser else UserProfile.Role.STANDARD
                }
            )
            if not created and user.is_superuser and profile.role != UserProfile.Role.ADMIN:
                profile.role = UserProfile.Role.ADMIN
                profile.save()
            
        self.stdout.write(self.style.SUCCESS('Successfully fixed user profiles'))