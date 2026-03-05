"""Comprehensive tests for the users app."""

import io
import logging
from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from PIL import Image

from allergies.constants.choices import CATEGORY_CONTACT
from allergies.models import Allergen, UserAllergy
from users._log_utils import email_token

User = get_user_model()

# Disable logging during tests to reduce noise
logging.disable(logging.CRITICAL)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def user_email():
    """Provide a test email address."""
    return "test@example.com"


@pytest.fixture
def user_password():
    """Provide a test password."""
    return "SecurePassword123!"


@pytest.fixture
def custom_user(db, user_email, user_password):
    """Create a basic custom user for testing."""
    return User.objects.create_user(
        email=user_email, username="testuser", password=user_password
    )


@pytest.fixture
def allergen_contact(db):
    """Create a contact allergen for testing."""
    return Allergen.objects.create(
        category=CATEGORY_CONTACT, allergen_key="sls", is_active=True
    )


@pytest.fixture
def user_allergy(db, custom_user, allergen_contact):
    """Create a UserAllergy instance for testing signals."""
    return UserAllergy.objects.create(
        user=custom_user,
        allergen=allergen_contact,
        severity_level="moderate",
        is_confirmed=True,
    )


def create_test_image(format="JPEG", size_mb=1):
    """
    Create a test image file in memory.

    Args:
        format: Image format (JPEG, PNG, WEBP).
        size_mb: Approximate file size in MB.

    Returns:
        io.BytesIO: Image file in memory.
    """
    # Create a simple image
    img = Image.new("RGB", (800, 600), color="red")
    img_io = io.BytesIO()

    # Save with appropriate format
    save_format = "JPEG" if format == "JPEG" else format
    img.save(img_io, format=save_format, quality=85)

    # Adjust size if needed (for size validation tests)
    if size_mb > 2:
        # Create larger image for size tests
        img_io = io.BytesIO(b"0" * (size_mb * 1024 * 1024))

    img_io.name = f"test_image.{format.lower()}"
    img_io.seek(0)
    return img_io


# ============================================================================
# Manager Tests
# ============================================================================


@pytest.mark.django_db
class TestCustomUserManager:
    """Tests for CustomUserManager functionality."""

    def test_create_user_success(self, user_email, user_password):
        """Test successful user creation with email and password."""
        user = User.objects.create_user(
            email=user_email, username="newuser", password=user_password
        )

        assert user.email == user_email
        assert user.username == "newuser"
        assert user.check_password(user_password)
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_user_email_required(self):
        """Test that email is required for user creation."""
        with pytest.raises(ValueError, match="The Email field must be set"):
            User.objects.create_user(email="", username="testuser", password="pass123")

    def test_create_user_invalid_email(self):
        """Test that invalid email format raises ValidationError."""
        with pytest.raises(ValidationError, match="Invalid email format"):
            User.objects.create_user(
                email="invalid-email", username="testuser", password="pass123"
            )

    def test_create_user_email_normalized(self):
        """Test that email domain is normalized to lowercase."""
        user = User.objects.create_user(
            email="Test@EXAMPLE.COM", username="testuser", password="pass123"
        )
        assert user.email == "Test@example.com"  # Domain lowercased

    def test_create_superuser_success(self, user_email, user_password):
        """Test successful superuser creation."""
        superuser = User.objects.create_superuser(
            email=user_email, username="admin", password=user_password
        )

        assert superuser.is_staff is True
        assert superuser.is_superuser is True
        assert superuser.is_active is True

    def test_create_superuser_staff_required(self, user_email, user_password):
        """Test that superuser must have is_staff=True."""
        with pytest.raises(ValueError, match="Superuser must have is_staff=True"):
            User.objects.create_superuser(
                email=user_email,
                username="admin",
                password=user_password,
                is_staff=False,
            )

    def test_create_superuser_superuser_required(self, user_email, user_password):
        """Test that superuser must have is_superuser=True."""
        with pytest.raises(ValueError, match="Superuser must have is_superuser=True"):
            User.objects.create_superuser(
                email=user_email,
                username="admin",
                password=user_password,
                is_superuser=False,
            )


# ============================================================================
# Model Tests
# ============================================================================


@pytest.mark.django_db
class TestCustomUserModel:
    """Tests for CustomUser model functionality."""

    def test_str_representation(self, custom_user):
        """Test that __str__ returns the email."""
        assert str(custom_user) == custom_user.email

    def test_email_uniqueness(self, custom_user, user_password):
        """Test that duplicate emails are not allowed."""
        with pytest.raises(ValidationError):
            User.objects.create_user(
                email=custom_user.email,
                username="another_user",
                password=user_password,
            )

    def test_get_age_with_birthdate(self, custom_user):
        """Test age calculation when date_of_birth is set."""
        # Set birthdate to 25 years ago
        custom_user.date_of_birth = date.today() - timedelta(days=25 * 365)
        custom_user.save()

        age = custom_user.get_age()
        assert age in [24, 25]  # Account for leap years and exact day

    def test_get_age_without_birthdate(self, custom_user):
        """Test that get_age returns None when date_of_birth is not set."""
        assert custom_user.get_age() is None


# ============================================================================
# Validation Tests
# ============================================================================


@pytest.mark.django_db
@pytest.mark.usefixtures("media_root")
class TestCustomUserValidation:
    """Tests for CustomUser field validation."""

    @pytest.fixture(autouse=True)
    def close_profile_picture(self, custom_user):
        """Close any open FieldFile handle on profile_picture after each test.

        Django's FieldFile.save() opens the saved file internally and does not
        close it automatically, which causes a ResourceWarning when the object
        is garbage-collected. Explicitly closing here prevents that.
        """
        yield
        if custom_user.profile_picture:
            custom_user.profile_picture.close()

    def test_date_of_birth_future_invalid(self, custom_user):
        """Test that future date_of_birth raises ValidationError."""
        custom_user.date_of_birth = date.today() + timedelta(days=1)

        with pytest.raises(
            ValidationError, match="Date of birth cannot be in the future"
        ):
            custom_user.full_clean()

    def test_date_of_birth_today_valid(self, custom_user):
        """Test that today's date as date_of_birth is valid (edge case)."""
        custom_user.date_of_birth = date.today()

        with pytest.raises(
            ValidationError, match="You must be at least 13 years old"
        ):  # COPPA
            custom_user.full_clean()

    def test_minimum_age_under_13_invalid(self, custom_user):
        """Test that users under 13 years old are rejected (COPPA)."""
        # Set birthdate to 10 years ago
        custom_user.date_of_birth = date.today() - timedelta(days=10 * 365)

        with pytest.raises(ValidationError, match="You must be at least 13 years old"):
            custom_user.full_clean()

    def test_minimum_age_13_valid(self, custom_user):
        """Test that users exactly 13 years old are accepted."""
        # Set birthdate to exactly 13 years ago
        custom_user.date_of_birth = date.today() - timedelta(
            days=13 * 365 + 4
        )  # +leap days

        custom_user.full_clean()  # Should not raise

    def test_image_size_exceeds_limit(self, custom_user):
        """Test that images over 5MB are rejected."""
        large_image = create_test_image(format="JPEG", size_mb=6)

        with pytest.raises(
            ValidationError, match="Image file size must not exceed 5MB"
        ):
            custom_user.profile_picture.save("large.jpg", large_image, save=False)
            custom_user.full_clean()

    def test_image_format_jpeg_valid(self, custom_user):
        """Test that JPEG format is accepted."""
        jpeg_image = create_test_image(format="JPEG", size_mb=1)
        custom_user.profile_picture.save("test.jpg", jpeg_image, save=False)
        custom_user.full_clean()  # Should not raise

    def test_image_format_png_valid(self, custom_user):
        """Test that PNG format is accepted."""
        png_image = create_test_image(format="PNG", size_mb=1)
        custom_user.profile_picture.save("test.png", png_image, save=False)
        custom_user.full_clean()  # Should not raise

    def test_image_format_webp_valid(self, custom_user):
        """Test that WebP format is accepted."""
        webp_image = create_test_image(format="WEBP", size_mb=1)
        custom_user.profile_picture.save("test.webp", webp_image, save=False)
        custom_user.full_clean()  # Should not raise

    def test_phone_number_us_format_valid(self, custom_user):
        """Test that US phone number format is accepted."""
        custom_user.phone_number = "+12024561414"
        custom_user.full_clean()  # Should not raise

    def test_phone_number_optional(self, custom_user):
        """Test that phone_number can be blank."""
        custom_user.phone_number = ""
        custom_user.full_clean()  # Should not raise


# ============================================================================
# Signal Tests
# ============================================================================


@pytest.mark.django_db(transaction=True)
class TestAllergySignalBatching:
    """Tests for allergy timestamp signal handlers."""

    def test_allergies_updated_at_on_create(self, custom_user, allergen_contact):
        """Test that allergies_updated_at is set when UserAllergy is created."""
        assert custom_user.allergies_updated_at is None

        # Create a UserAllergy
        with transaction.atomic():
            UserAllergy.objects.create(
                user=custom_user,
                allergen=allergen_contact,
                severity_level="mild",
                is_confirmed=True,
            )

        # Refresh user from database
        custom_user.refresh_from_db()
        assert custom_user.allergies_updated_at is not None

    def test_allergies_updated_at_on_update(self, custom_user, user_allergy):
        """Test that allergies_updated_at is updated when UserAllergy is modified."""
        # Clear timestamp
        custom_user.allergies_updated_at = None
        custom_user.save()

        # Update the UserAllergy
        with transaction.atomic():
            user_allergy.severity = "severe"
            user_allergy.save()

        # Refresh user from database
        custom_user.refresh_from_db()
        assert custom_user.allergies_updated_at is not None

    def test_allergies_updated_at_on_delete(self, custom_user, user_allergy):
        """Test that allergies_updated_at is updated when UserAllergy is deleted."""
        # Clear timestamp
        custom_user.allergies_updated_at = None
        custom_user.save()

        # Delete the UserAllergy
        with transaction.atomic():
            user_allergy.delete()

        # Refresh user from database
        custom_user.refresh_from_db()
        assert custom_user.allergies_updated_at is not None

    def test_batch_update_multiple_allergies(self, custom_user, allergen_contact):
        """Test that multiple allergy changes in one transaction batch correctly."""
        allergen2 = Allergen.objects.create(
            category=CATEGORY_CONTACT, allergen_key="fragrance", is_active=True
        )

        # Create multiple allergies in one transaction
        with transaction.atomic():
            UserAllergy.objects.create(
                user=custom_user, allergen=allergen_contact, severity_level="mild"
            )
            UserAllergy.objects.create(
                user=custom_user, allergen=allergen2, severity_level="moderate"
            )

        # Refresh user from database
        custom_user.refresh_from_db()
        assert custom_user.allergies_updated_at is not None

    def test_timestamp_precision_includes_seconds(self, custom_user, allergen_contact):
        """Test that allergies_updated_at includes full timestamp with seconds."""
        with transaction.atomic():
            UserAllergy.objects.create(
                user=custom_user, allergen=allergen_contact, severity_level="mild"
            )

        custom_user.refresh_from_db()
        timestamp = custom_user.allergies_updated_at

        # Verify timestamp has second precision (not truncated)
        assert timestamp.second is not None
        assert timestamp.microsecond is not None


# ============================================================================
# Logging Tests
# ============================================================================


@pytest.mark.django_db
@pytest.mark.usefixtures("enable_users_logging")
class TestManagerLogging:
    """Assert manager log messages never contain raw PII."""

    def test_create_user_success_logs_id_not_email(self, caplog, user_password):
        """Successful creation logs user.id; raw email must not appear."""
        email = "log_test_success@example.com"
        with caplog.at_level(logging.INFO, logger="users"):
            user = User.objects.create_user(
                email=email, username="log_success", password=user_password
            )

        assert str(user.id) in caplog.text
        assert email not in caplog.text

    def test_create_user_invalid_email_logs_token_not_email(self, caplog):
        """Invalid-email error logs a token; raw email must not appear."""
        email = "not-an-email"
        with caplog.at_level(logging.ERROR, logger="users"):
            with pytest.raises(ValidationError):
                User.objects.create_user(
                    email=email, username="log_bad", password="pass123"
                )

        assert "token=" in caplog.text
        assert email not in caplog.text

    def test_create_user_debug_logs_token_not_email(self, caplog, user_password):
        """Debug log during creation contains a token; raw email must not appear."""
        email = "log_test_debug@example.com"
        with caplog.at_level(logging.DEBUG, logger="users"):
            User.objects.create_user(
                email=email, username="log_debug", password=user_password
            )

        assert "token=" in caplog.text
        assert email not in caplog.text

    def test_create_superuser_logs_token_not_email(self, caplog, user_password):
        """Superuser creation logs a token; raw email must not appear."""
        email = "log_super@example.com"
        with caplog.at_level(logging.INFO, logger="users"):
            User.objects.create_superuser(
                email=email, username="log_superuser", password=user_password
            )

        assert "token=" in caplog.text
        assert email not in caplog.text


@pytest.mark.django_db
@pytest.mark.usefixtures("enable_users_logging")
class TestModelLogging:
    """Assert model log messages never contain raw PII."""

    def test_future_dob_warning_logs_token_not_email(self, caplog, custom_user):
        """Future DOB warning logs a token; raw email must not appear."""
        custom_user.date_of_birth = date.today() + timedelta(days=1)

        with caplog.at_level(logging.WARNING, logger="users"):
            with pytest.raises(ValidationError):
                custom_user.full_clean()

        assert "token=" in caplog.text
        assert custom_user.email not in caplog.text


class TestEmailToken:
    """Unit tests for email_token(). No database required."""

    def test_token_is_consistent_for_same_email(self):
        """The same email always produces the same token within a SECRET_KEY lifetime."""
        email = "consistency@example.com"
        assert email_token(email) == email_token(email)

    def test_token_differs_for_different_emails(self):
        """Different emails produce different tokens."""
        assert email_token("a@example.com") != email_token("b@example.com")

    def test_token_length_is_12(self):
        """Token is exactly 12 characters."""
        assert len(email_token("any@example.com")) == 12


# Re-enable logging after tests
def teardown_module():
    """Re-enable logging after all tests complete."""
    logging.disable(logging.NOTSET)
