"""Shared pytest fixtures for all apps.

This module provides reusable fixtures available to all test files in the project.
Fixtures are organized by category: users, allergens, and authentication.
"""

import pytest
from django.contrib.auth import get_user_model

from allergies.constants.choices import CATEGORY_CONTACT, CATEGORY_FOOD
from allergies.models import Allergen, UserAllergy

User = get_user_model()


# ============================================================================
# User Fixtures
# ============================================================================


@pytest.fixture
def user_email():
    """Provide a standard test email address."""
    return "test@example.com"


@pytest.fixture
def user_password():
    """Provide a standard test password for all test users."""
    return "SecurePassword123!"


@pytest.fixture
def test_user(db, user_email, user_password):
    """Create a standard test user with predictable credentials.

    Returns:
        User: A CustomUser instance with username='testuser',
              email='test@example.com', password='SecurePassword123!'
    """
    return User.objects.create_user(
        email=user_email, username="testuser", password=user_password
    )


@pytest.fixture
def custom_user(db, user_email, user_password):
    """Alias for test_user fixture for backward compatibility.

    This fixture exists to support existing tests that use 'custom_user'.
    New tests should use 'test_user' instead.
    """
    return User.objects.create_user(
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
    client.login(username=test_user.username, password=user_password)
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
def allergen_contact(db):
    """Alias for contact_allergen fixture for backward compatibility.

    This fixture exists to support existing tests that use 'allergen_contact'.
    New tests should use 'contact_allergen' instead.
    """
    return Allergen.objects.create(
        category=CATEGORY_CONTACT, allergen_key="sls", is_active=True
    )


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
def allergen_food(db):
    """Alias for food_allergen fixture for backward compatibility.

    This fixture exists to support existing tests that use 'allergen_food'.
    New tests should use 'food_allergen' instead.
    """
    return Allergen.objects.create(
        category=CATEGORY_FOOD, allergen_key="peanut", is_active=True
    )


# ============================================================================
# UserAllergy Fixtures
# ============================================================================


@pytest.fixture
def user_allergy(db, test_user, contact_allergen):
    """Create a UserAllergy instance linking test_user to contact_allergen.

    Returns:
        UserAllergy: UserAllergy with severity='moderate', confirmed=True
    """
    return UserAllergy.objects.create(
        user=test_user,
        allergen=contact_allergen,
        severity="moderate",
        confirmed=True,
    )
