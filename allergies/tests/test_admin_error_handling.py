import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from allergies.admin import AllergenAdmin
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
            category="fragrance", allergen_key="lavender", is_active=True
        )
        allergen2 = Allergen.objects.create(
            category="fragrance", allergen_key="rose", is_active=True
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

    def test_deactivate_allergens_logs_admin_id(self, caplog):
        """Focus purely on log content integrity and PII exclusion."""
        Allergen.objects.create(category="fragrance", allergen_key="t1", is_active=True)
        Allergen.objects.create(category="fragrance", allergen_key="t2", is_active=True)

        request = self._prepare_request()
        queryset = Allergen.objects.all()

        with caplog.at_level("INFO", logger="allergies.admin"):
            self.admin.deactivate_allergens(request, queryset)

        assert str(self.superuser.id) in caplog.text
        assert self.superuser.email not in caplog.text

        log_output_lower = caplog.text.lower()
        assert "deactivating 2" in log_output_lower
        assert "successfully deactivated 2" in log_output_lower

    def test_activate_allergens_success(self):
        """Test functional bulk activation of allergens."""
        allergen = Allergen.objects.create(
            category="preservative", allergen_key="parabens", is_active=False
        )

        request = self._prepare_request()
        queryset = Allergen.objects.filter(id=allergen.id)

        self.admin.activate_allergens(request, queryset)

        allergen.refresh_from_db()
        assert allergen.is_active
