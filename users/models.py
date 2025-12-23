from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    """Custom user model extending Django's AbstractUser.
    Additional fields can be added here in the future.
    """

    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
