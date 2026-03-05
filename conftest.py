"""Shared pytest fixtures for all apps.

This module provides reusable fixtures available to all test files in the project.
Fixtures are organized by category: users, allergens, and authentication.
"""

import logging
import warnings

import pytest
from django.contrib.auth import get_user_model

from allergies.constants.choices import CATEGORY_CONTACT, CATEGORY_FOOD
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


@pytest.fixture
def custom_user(test_user):
    """Alias for test_user fixture for backward compatibility.

    This fixture exists to support existing tests that use 'custom_user'.
    New tests should use 'test_user' instead.
    """
    warnings.warn(
        "custom_user is deprecated; use test_user instead. Will be removed in v1.0.0.",
        DeprecationWarning,
        stacklevel=2,
    )
    return test_user


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
                  allergen_key='sls', is_active=True
    """
    return Allergen.objects.create(
        category=CATEGORY_CONTACT, allergen_key="sls", is_active=True
    )


@pytest.fixture
def allergen_contact(contact_allergen):
    """Alias for contact_allergen fixture for backward compatibility.

    This fixture exists to support existing tests that use 'allergen_contact'.
    New tests should use 'contact_allergen' instead.
    """
    warnings.warn(
        "allergen_contact is deprecated; use contact_allergen instead. Will be removed in v1.0.0.",
        DeprecationWarning,
        stacklevel=2,
    )
    return contact_allergen


@pytest.fixture
def food_allergen(db):
    """Create a food allergen: Peanut.

    Returns:
        Allergen: Food allergen with category='food',
                  allergen_key='peanut', is_active=True
    """
    return Allergen.objects.create(
        category=CATEGORY_FOOD, allergen_key="peanut", is_active=True
    )


@pytest.fixture
def allergen_food(food_allergen):
    """Alias for food_allergen fixture for backward compatibility.

    This fixture exists to support existing tests that use 'allergen_food'.
    New tests should use 'food_allergen' instead.
    """
    warnings.warn(
        "allergen_food is deprecated; use food_allergen instead. Will be removed in v1.0.0.",
        DeprecationWarning,
        stacklevel=2,
    )
    return food_allergen


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
    """Re-enable logging and attach caplog's handler directly to the 'users' logger.

    Django's LOGGING config sets propagate=False on the 'users' logger, so
    records never reach caplog's root-level handler. Attaching caplog.handler
    directly avoids mutating the propagation flag — production logging config
    stays intact.
    """
    logging.disable(logging.NOTSET)
    users_logger = logging.getLogger("users")
    users_logger.addHandler(caplog.handler)
    yield
    users_logger.removeHandler(caplog.handler)
    logging.disable(logging.CRITICAL)
