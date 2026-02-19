"""Custom user model for the skincare filter application."""

import logging
from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager
from .validators import validate_image_format, validate_image_size, validate_minimum_age

# Module-level logger setup
logger = logging.getLogger(__name__)


class CustomUser(AbstractUser):
    """
    Custom user model with extended profile and health tracking fields.

    Uses email as the primary authentication identifier instead of username.
    Includes profile information, contact details, and allergy tracking timestamp.
    """

    # Authentication & Identity
    email = models.EmailField(
        unique=True,
        blank=False,
        help_text="Email address used for authentication",
    )

    # Profile Information
    bio = models.TextField(
        blank=True,
        default="",
        help_text="User biography or personal description",
    )

    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        help_text="Contact phone number (US format: (555) 123-4567)",
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text="Date of birth (must be at least 13 years old)",
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/%Y/%m/",
        blank=True,
        null=True,
        max_length=255,
        validators=[validate_image_size, validate_image_format],
        help_text="Profile picture (JPEG, PNG, or WebP only. Max 5MB)",
    )

    # Health & Allergy Tracking
    allergies_updated_at = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
        help_text="Timestamp of last allergy profile modification (auto-managed)",
    )

    # Authentication Configuration
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # Custom Manager
    objects = CustomUserManager()

    class Meta:
        db_table = "users_customuser"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        """Return string representation of the user."""
        return self.email

    def clean(self) -> None:
        """
        Validate model fields before saving.

        Validates:
        - Date of birth is not in the future
        - User meets minimum age requirement (13 years)

        Raises:
            ValidationError: If validation fails.
        """
        super().clean()

        # Validate date_of_birth
        if self.date_of_birth:
            today = timezone.now().date()

            # Check if date is not in the future
            if self.date_of_birth > today:
                logger.warning(
                    f"User {self.email} validation failed: date_of_birth {self.date_of_birth} is in the future"
                )
                raise ValidationError(
                    {"date_of_birth": "Date of birth cannot be in the future."}
                )

            # Check minimum age requirement (COPPA compliance)
            validate_minimum_age(self.date_of_birth)

    def save(self, *args, **kwargs) -> None:
        """
        Override save to ensure validation always runs.

        Calls full_clean() before saving to enforce model-level validation.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def age(self) -> int | None:
        """
        Calculate and return the user's age in years.

        Returns:
            int | None: Age in years, or None if date_of_birth is not set.
        """
        if not self.date_of_birth:
            return None

        today = timezone.now().date()
        age = today.year - self.date_of_birth.year

        # Adjust if birthday hasn't occurred this year yet
        if (today.month, today.day) < (
            self.date_of_birth.month,
            self.date_of_birth.day,
        ):
            age -= 1

        return age
