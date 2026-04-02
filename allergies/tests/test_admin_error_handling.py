import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from allergies.admin import AllergenAdmin
from allergies.constants.compounds import CATEGORY_CONTACT
from allergies.models import Allergen
from users.models import CustomUser


@pytest.mark.django_db
@pytest.mark.usefixtures("enable_allergies_logging")
class TestAllergenAdminActions:
    """Test error handling and logging in AllergenAdmin actions."""

    def setup_method(self):
        """Set up test fixtures."""
        self.factory = RequestFactory()
        self.admin = AllergenAdmin(Allergen, AdminSite())
        # Use a realistic birth date to satisfy the full_clean() call in CustomUser.save()
        self.superuser = CustomUser.objects.create_superuser(
            username="admin_user",
            password="admin123",
            email="admin@test.com",
            date_of_birth="1990-01-01",
        )

    def _prepare_request(self):
        """Helper to set up request with user, session, and messages."""
        request = self.factory.get("/")
        request.user = self.superuser

        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)
        return request

    def test_deactivate_allergens_success(self, caplog):
        """Test successful bulk deactivation and privacy-aware logging."""
        allergen1 = Allergen.objects.create(
            category=CATEGORY_CONTACT, allergen_key="t1", is_active=True
        )
        allergen2 = Allergen.objects.create(
            category=CATEGORY_CONTACT, allergen_key="t2", is_active=True
        )

        request = self._prepare_request()
        queryset = Allergen.objects.filter(id__in=[allergen1.id, allergen2.id])

        with caplog.at_level("INFO", logger="allergies.admin"):
            self.admin.deactivate_allergens(request, queryset)

        allergen1.refresh_from_db()
        allergen2.refresh_from_db()
        assert not allergen1.is_active
        assert not allergen2.is_active

        # Assertions for the logs in allergies/admin.py
        log_text = caplog.text
        assert str(self.superuser.id) in log_text
        # Ensure the CustomUser.email identifier is NOT leaked in admin logs
        assert self.superuser.email not in log_text
        assert self.superuser.username not in log_text
        assert "deactivating 2" in log_text.lower()
        assert "successfully deactivated 2" in log_text.lower()

    def test_activate_allergens_success(self):
        """Test functional bulk activation of allergens."""
        allergen = Allergen.objects.create(
            category=CATEGORY_CONTACT, allergen_key="t3", is_active=False
        )

        request = self._prepare_request()
        queryset = Allergen.objects.filter(id=allergen.id)

        self.admin.activate_allergens(request, queryset)

        allergen.refresh_from_db()
        assert allergen.is_active

    def test_deactivate_allergens_error_path(self, caplog):
        """Test that exceptions in deactivate are caught and logged."""
        from unittest.mock import MagicMock

        request = self._prepare_request()
        mock_qs = MagicMock()
        mock_qs.count.return_value = 1
        mock_qs.update.side_effect = Exception("DB error")

        with caplog.at_level("ERROR", logger="allergies.admin"):
            self.admin.deactivate_allergens(request, mock_qs)

        assert "error deactivating" in caplog.text.lower()

    def test_activate_allergens_error_path(self, caplog):
        """Test that exceptions in activate are caught and logged."""
        from unittest.mock import MagicMock

        request = self._prepare_request()
        mock_qs = MagicMock()
        mock_qs.count.return_value = 1
        mock_qs.update.side_effect = Exception("DB error")

        with caplog.at_level("ERROR", logger="allergies.admin"):
            self.admin.activate_allergens(request, mock_qs)

        assert "error activating" in caplog.text.lower()


@pytest.mark.django_db
@pytest.mark.usefixtures("enable_allergies_logging")
class TestUserAllergyAdminActions:
    """Test mark_as_confirmed and mark_as_unconfirmed admin actions."""

    def setup_method(self):
        from allergies.admin import UserAllergyAdmin
        from allergies.models import UserAllergy

        self.factory = RequestFactory()
        self.admin = UserAllergyAdmin(UserAllergy, AdminSite())
        self.superuser = CustomUser.objects.create_superuser(
            username="ua_admin",
            password="admin123",
            email="ua_admin@test.com",
            date_of_birth="1990-01-01",
        )

    def _prepare_request(self):
        request = self.factory.get("/")
        request.user = self.superuser
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)
        return request

    def test_mark_as_confirmed_success(self, user_allergy):
        user_allergy.is_confirmed = False
        user_allergy.save()
        request = self._prepare_request()
        from allergies.models import UserAllergy

        qs = UserAllergy.objects.filter(pk=user_allergy.pk)
        self.admin.mark_as_confirmed(request, qs)
        user_allergy.refresh_from_db()
        assert user_allergy.is_confirmed is True

    def test_mark_as_unconfirmed_success(self, user_allergy):
        user_allergy.is_confirmed = True
        user_allergy.save()
        request = self._prepare_request()
        from allergies.models import UserAllergy

        qs = UserAllergy.objects.filter(pk=user_allergy.pk)
        self.admin.mark_as_unconfirmed(request, qs)
        user_allergy.refresh_from_db()
        assert user_allergy.is_confirmed is False

    def test_mark_as_confirmed_error_path(self, caplog):
        from unittest.mock import MagicMock

        request = self._prepare_request()
        mock_qs = MagicMock()
        mock_qs.count.return_value = 1
        mock_qs.update.side_effect = Exception("DB error")
        with caplog.at_level("ERROR", logger="allergies.admin"):
            self.admin.mark_as_confirmed(request, mock_qs)
        assert "error confirming" in caplog.text.lower()

    def test_mark_as_unconfirmed_error_path(self, caplog):
        from unittest.mock import MagicMock

        request = self._prepare_request()
        mock_qs = MagicMock()
        mock_qs.count.return_value = 1
        mock_qs.update.side_effect = Exception("DB error")
        with caplog.at_level("ERROR", logger="allergies.admin"):
            self.admin.mark_as_unconfirmed(request, mock_qs)
        assert "error unconfirming" in caplog.text.lower()
