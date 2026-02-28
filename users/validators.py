"""Validators for the users app."""

import logging
from datetime import date

from django.core.exceptions import ValidationError
from django.utils import timezone
from PIL import Image

# Module-level logger setup
logger = logging.getLogger(__name__)

# Constants
MAX_IMAGE_SIZE_MB = 5
MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024
ALLOWED_IMAGE_FORMATS = ["JPEG", "PNG", "WEBP"]
MINIMUM_AGE_YEARS = 13


def validate_image_size(image) -> None:
    """
    Validate that the uploaded image does not exceed the maximum file size.

    Args:
        image: The uploaded image file (UploadedFile or InMemoryUploadedFile).

    Raises:
        ValidationError: If the image size exceeds MAX_IMAGE_SIZE_MB.
    """
    if image.size > MAX_IMAGE_SIZE_BYTES:
        logger.warning(
            f"Image upload rejected: size {image.size} bytes exceeds {MAX_IMAGE_SIZE_MB}MB limit"
        )
        raise ValidationError(
            f"Image file size must not exceed {MAX_IMAGE_SIZE_MB}MB. "
            f"Your file is {image.size / (1024 * 1024):.2f}MB."
        )


def validate_image_format(image) -> None:
    """
    Validate that the uploaded image is in an allowed format (JPEG, PNG, or WebP).

    Args:
        image: The uploaded image file (UploadedFile or InMemoryUploadedFile).

    Raises:
        ValidationError: If the image format is not in ALLOWED_IMAGE_FORMATS.
    """
    try:
        # Open the image to verify format; context manager ensures the file handle is closed
        with Image.open(image) as img:
            image_format = img.format

        if image_format not in ALLOWED_IMAGE_FORMATS:
            logger.warning(
                f"Image upload rejected: format '{image_format}' not in allowed formats {ALLOWED_IMAGE_FORMATS}"
            )
            raise ValidationError(
                f"Unsupported image format '{image_format}'. "
                f"Allowed formats: {', '.join(ALLOWED_IMAGE_FORMATS)}."
            )

        # Reset file pointer after Pillow has finished reading
        image.seek(0)

    except (OSError, AttributeError) as e:
        logger.error(f"Error validating image format: {e}", exc_info=True)
        raise ValidationError(
            "Unable to process image file. Please ensure it is a valid image."
        ) from e


def validate_minimum_age(date_of_birth: date) -> None:
    """
    Validate that the user meets the minimum age requirement (COPPA compliance).

    Args:
        date_of_birth: The user's date of birth.

    Raises:
        ValidationError: If the user is under MINIMUM_AGE_YEARS old.
    """
    if not date_of_birth:
        return  # Allow None/null values (field is optional)

    today = timezone.now().date()
    age_in_days = (today - date_of_birth).days
    age_in_years = age_in_days / 365.25  # Account for leap years

    if age_in_years < MINIMUM_AGE_YEARS:
        logger.warning(
            f"User registration rejected: age {age_in_years:.1f} years is below minimum {MINIMUM_AGE_YEARS}"
        )
        raise ValidationError(
            f"You must be at least {MINIMUM_AGE_YEARS} years old to use this service. "
            f"Please verify your date of birth."
        )
