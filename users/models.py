from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Additional fields can be added here in the future.
    """
    # model definition necessary for relationships in other apps
    date_of_birth = models.DateField(null=True, blank=True)
    
    # !! IMPORTANT: Explicitly set related_name to avoid clashes
    # !! when replacing the default User model in Django
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permission_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def __str__(self):
        return self.username