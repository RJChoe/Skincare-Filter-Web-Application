"""Shared pytest fixtures for all apps.

This module provides reusable fixtures available to all test files in the project.
Fixtures are organized by category: users, allergens, and authentication.
"""

import logging

import pytest
from django.contrib.auth import get_user_model

from allergies.constants.compounds import CATEGORY_CONTACT
from allergies.models import Allergen, UserAllergy
from users.models import CustomUser

User = get_user_model()


@pytest.fixture
def media_root(settings, tmp_path_factory):
    """Redirect MEDIA_ROOT to a pytest-managed temp directory for this test.

    Prevents profile picture uploads from writing into the real project
    media/ folder during tests. The temporary directory is automatically
    removed by pytest after the test completes, even on hard failures.
    """
    temp_media = tmp_path_factory.mktemp("media")
    settings.MEDIA_ROOT = str(temp_media)
    yield temp_media


# ============================================================================
# User Fixtures
# ============================================================================


@pytest.fixture(scope="session")
def user_email():
    """Provide a standard test email address."""
    return "test@example.com"


@pytest.fixture(scope="session")
def user_password():
    """Provide a standard test password for all test users."""
    return "SecurePassword123!"


@pytest.fixture
def test_user(db, user_email, user_password) -> CustomUser:
    """Create a standard test user with predictable credentials.

    Returns:
        CustomUser: A CustomUser instance with username='testuser',
              email='test@example.com', password='SecurePassword123!'
    """
    return CustomUser.objects.create_user(
        email=user_email, username="testuser", password=user_password
    )


# ============================================================================
# Authentication Fixtures
# ============================================================================


@pytest.fixture
def authenticated_client(client, test_user, user_password):
    """Django test client with authenticated session.

    Returns:
        Client: Django test client logged in as test_user
    """
    client.login(email=test_user.email, password=user_password)
    return client


# ============================================================================
# Allergen Fixtures
# ============================================================================


@pytest.fixture
def contact_allergen(db):
    """Create a contact allergen: Sodium Lauryl Sulfate (SLS).

    Returns:
        Allergen: Contact allergen with category='contact',
                  allergen_key='sodium_lauryl_sulfate', is_active=True
    """
    # get_or_create: seed migration pre-populates this key; create() would
    # raise IntegrityError in transaction=True tests where flush doesn't run
    allergen, _ = Allergen.objects.get_or_create(
        category=CATEGORY_CONTACT,
        allergen_key="sodium_lauryl_sulfate",
        defaults={
            "label": "Sodium Lauryl Sulfate (SLS)",
            "subcategory": "Surfactants & Emulsifiers",
            "is_active": True,
        },
    )
    return allergen


@pytest.fixture
def second_contact_allergen(db):
    """Create a contact allergen: Methylparaben.

    Returns:
        Allergen: Contact allergen with category='contact',
                  allergen_key='methylparaben', is_active=True
    """
    # get_or_create: same reason as contact_allergen above
    allergen, _ = Allergen.objects.get_or_create(
        category=CATEGORY_CONTACT,
        allergen_key="methylparaben",
        defaults={
            "label": "Methylparaben",
            "subcategory": "Preservatives",
            "is_active": True,
        },
    )
    return allergen


# ============================================================================
# UserAllergy Fixtures
# ============================================================================


@pytest.fixture
def user_allergy(test_user, contact_allergen):
    """Create a confirmed UserAllergy instance linking test_user to contact_allergen.

    Returns:
        UserAllergy: UserAllergy with severity_level='moderate', is_confirmed=True
    """
    return UserAllergy.objects.create(
        user=test_user,
        allergen=contact_allergen,
        severity_level="moderate",
        is_confirmed=True,
    )


@pytest.fixture
def unconfirmed_user_allergy(test_user, contact_allergen):
    """Create an unconfirmed UserAllergy instance linking test_user to contact_allergen.

    Represents a newly added allergy that has not yet been verified. Uses model
    defaults: is_confirmed=False and severity_level='' (blank).

    Returns:
        UserAllergy: UserAllergy with severity_level='', is_confirmed=False
    """
    return UserAllergy.objects.create(
        user=test_user,
        allergen=contact_allergen,
    )


# ============================================================================
# Logging Fixtures
# ============================================================================


@pytest.fixture
def enable_users_logging(caplog):
    """Attach caplog's handler to the 'users' logger for log-assertion tests.

    Does not touch logging.disable() — uses logger-level gating instead,
    which is test-local and safe for parallel execution.
    """
    users_logger = logging.getLogger("users")
    original_level = users_logger.level
    users_logger.setLevel(logging.DEBUG)
    users_logger.addHandler(caplog.handler)
    yield
    users_logger.removeHandler(caplog.handler)
    users_logger.setLevel(original_level)


@pytest.fixture
def enable_allergies_logging(caplog):
    """Attach caplog's handler to the 'allergies' logger for log-assertion tests."""
    allergies_logger = logging.getLogger("allergies")
    original_level = allergies_logger.level
    allergies_logger.setLevel(logging.DEBUG)
    allergies_logger.addHandler(caplog.handler)
    yield
    allergies_logger.removeHandler(caplog.handler)
    allergies_logger.setLevel(original_level)
