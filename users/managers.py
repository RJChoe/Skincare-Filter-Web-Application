"""Custom user manager for email-based authentication."""

import logging
from typing import Any

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# Module-level logger setup
logger = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for the CustomUser model.

    Provides methods to create regular users and superusers with email-based authentication.
    """

    def create_user(
        self,
        email: str,
        username: str,
        password: str | None = None,
        **extra_fields: Any,
    ):
        """
        Create and save a regular user with the given email, username, and password.

        Args:
            email: The user's email address (used as USERNAME_FIELD).
            username: The user's username.
            password: The user's password (optional, can be set later).
            **extra_fields: Additional fields to set on the user model.

        Returns:
            CustomUser: The created user instance.

        Raises:
            ValueError: If email is not provided.
            ValidationError: If email format is invalid.
        """
        if not email:
            logger.error("User creation failed: email is required")
            raise ValueError("The Email field must be set")

        # Validate email format
        try:
            validate_email(email)
        except ValidationError as e:
            logger.error(f"User creation failed: invalid email format '{email}'")
            raise ValidationError(f"Invalid email format: {e}") from e

        # Normalize email (lowercase domain)
        email = self.normalize_email(email)
        logger.debug(f"Creating user with email: {email}, username: {username}")

        # Create user instance
        user = self.model(email=email, username=username, **extra_fields)

        # Set password (hashed)
        user.set_password(password)

        try:
            user.save(using=self._db)
            logger.info(f"User created successfully: {user.id} ({email})")
            return user
        except Exception as e:
            logger.error(f"Failed to save user {email}: {e}", exc_info=True)
            raise

    def create_superuser(
        self,
        email: str,
        username: str,
        password: str | None = None,
        **extra_fields: Any,
    ):
        """
        Create and save a superuser with the given email, username, and password.

        Args:
            email: The superuser's email address.
            username: The superuser's username.
            password: The superuser's password.
            **extra_fields: Additional fields to set on the user model.

        Returns:
            CustomUser: The created superuser instance.

        Raises:
            ValueError: If is_staff or is_superuser is not True.
        """
        # Set required superuser flags
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # Validate superuser flags
        if extra_fields.get("is_staff") is not True:
            logger.error("Superuser creation failed: is_staff must be True")
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            logger.error("Superuser creation failed: is_superuser must be True")
            raise ValueError("Superuser must have is_superuser=True.")

        logger.info(f"Creating superuser with email: {email}")
        return self.create_user(email, username, password, **extra_fields)
