import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory

from allergies.admin import AllergenAdmin, UserAllergyAdmin
from allergies.models import Allergen
from users.models import CustomUser


@pytest.mark.django_db
class TestAllergenAdminActions:
    """Test error handling in AllergenAdmin actions."""

    def setup_method(self):
        """Set up test fixtures."""
        self.factory = RequestFactory()
        self.admin = AllergenAdmin(Allergen, AdminSite())
        self.superuser = CustomUser.objects.create_superuser(
            username="admin", password="admin123", email="admin@test.com"
        )

    def test_deactivate_allergens_success(self, caplog):
        """Test successful bulk deactivation with logging."""
        # Create test allergens
        allergen1 = Allergen.objects.create(
            category="fragrance", allergen_key="lavender", is_active=True
        )
        allergen2 = Allergen.objects.create(
            category="fragrance", allergen_key="rose", is_active=True
        )

        # Create mock request
        request = self.factory.get("/")
        request.user = self.superuser
        request._messages = FallbackStorage(request)

        # Get queryset and run action
        queryset = Allergen.objects.filter(id__in=[allergen1.id, allergen2.id])

        with caplog.at_level("INFO"):
            self.admin.deactivate_selected_allergens(request, queryset)

        # Verify allergens were deactivated
        allergen1.refresh_from_db()
        allergen2.refresh_from_db()
        assert not allergen1.is_active
        assert not allergen2.is_active

        # Verify logging occurred
        assert any(
            "deactivating 2 allergens" in record.message for record in caplog.records
        )
        assert any(
            "Successfully deactivated" in record.message for record in caplog.records
        )

    def test_activate_allergens_success(self):
        """Test successful bulk activation."""
        # Create inactive allergen
        allergen = Allergen.objects.create(
            category="preservative", allergen_key="parabens", is_active=False
        )

        request = self.factory.get("/")
        request.user = self.superuser
        request._messages = FallbackStorage(request)

        queryset = Allergen.objects.filter(id=allergen.id)
        self.admin.activate_selected_allergens(request, queryset)

        allergen.refresh_from_db()
        assert allergen.is_active
