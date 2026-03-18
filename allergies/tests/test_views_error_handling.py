import pytest
from django.test import Client
from django.urls import reverse

from users.models import CustomUser


@pytest.mark.django_db
@pytest.mark.usefixtures("enable_allergies_logging")
class TestAllergiesListErrorHandling:
    """Test error handling in allergies_list view."""

    def test_unauthenticated_user_redirected_to_login(self):
        """Unauthenticated users must be redirected to login (302)."""
        client = Client()
        response = client.get(reverse("allergies:list"))

        assert response.status_code == 302
        assert "/login/" in response["Location"]

    def test_authenticated_access_succeeds(self):
        """Authenticated users should access page successfully."""
        client = Client()
        _user = CustomUser.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="testpass123",
        )
        client.login(email="testuser@example.com", password="testpass123")

        response = client.get(reverse("allergies:list"))

        assert response.status_code == 200
        assert "allergies/allergies_list.html" in [t.name for t in response.templates]

    def test_logging_for_authenticated_user(
        self, authenticated_client, test_user, caplog
    ):
        """Verify logging occurs for authenticated access using fixtures."""
        # Use the allergies.views logger as defined in your logging architecture
        with caplog.at_level("INFO", logger="allergies.views"):
            response = authenticated_client.get(reverse("allergies:list"))

        # Verify authenticated access succeeded
        assert response.status_code == 200

        # Logging assertions for privacy and auditing
        # 1. Assert caplog.text contains the user's pk as a string
        assert str(test_user.pk) in caplog.text

        # 2. Assert caplog.text does not contain the user's email address
        assert test_user.email not in caplog.text

        # 3. Assert the log level INFO appears for the access event
        assert "INFO" in caplog.text

    def test_unauthenticated_redirect_contains_next_param(self):
        """Redirect URL must include ?next= so users land on allergies list after login."""
        client = Client()
        response = client.get(reverse("allergies:list"))

        assert "next=" in response["Location"]
