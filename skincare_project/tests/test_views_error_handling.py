from unittest.mock import MagicMock, patch

import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse

from allergies.exceptions import InvalidIngredientError


@pytest.mark.django_db
class TestProductViewErrorHandling:
    """Test error handling in skincare_project product view."""

    def test_get_returns_200(self, client):
        response = client.get(reverse("product"))
        assert response.status_code == 200

    def test_get_unexpected_error_returns_500(self, client):
        """Unexpected exceptions in GET handler must return 500."""
        with patch(
            "skincare_project.views.logger.info",
            side_effect=Exception("unexpected boom"),
        ):
            response = client.get(reverse("product"))
        assert response.status_code == 500
        assert (
            response.json()["error"]
            == "An unexpected error occurred. Please try again later."
        )

    def test_post_unauthenticated_returns_401_json(self, client):
        """Unauthenticated POST must return 401 JSON, not 500."""
        response = client.post(reverse("product"))
        assert response.status_code == 401
        assert response.json()["error"] == "Authentication required"

    def test_post_authenticated_returns_501(self, authenticated_client):
        """Authenticated POST to unimplemented handler must return 501."""
        response = authenticated_client.post(reverse("product"))
        assert response.status_code == 501

    def test_post_invalid_ingredient_returns_400_json(self, authenticated_client):
        """InvalidIngredientError must return 400 JSON, not 500."""
        with patch("skincare_project.views.logger") as mock_logger:
            mock_logger.info = MagicMock()
            # Raise on the first call (inside try block); return normally on the
            # second call (inside the except handler's logger.warning).
            mock_logger.warning = MagicMock(
                side_effect=[InvalidIngredientError("bad ingredient"), None]
            )
            response = authenticated_client.post(reverse("product"))
        assert response.status_code == 400
        assert "error" in response.json()

    def test_post_validation_error_returns_400_json(self, authenticated_client):
        """Django ValidationError must return 400 JSON, not 500."""
        with patch("skincare_project.views.logger") as mock_logger:
            mock_logger.info = MagicMock()
            mock_logger.warning = MagicMock(
                side_effect=[ValidationError("model validation failed"), None]
            )
            response = authenticated_client.post(reverse("product"))
        assert response.status_code == 400
        assert "error" in response.json()

    def test_post_unexpected_error_returns_500(self, authenticated_client):
        """Unexpected exceptions in POST handler must return 500."""
        with patch("skincare_project.views.logger") as mock_logger:
            mock_logger.info = MagicMock()
            mock_logger.warning = MagicMock(
                side_effect=[Exception("unexpected boom"), None]
            )
            response = authenticated_client.post(reverse("product"))
        assert response.status_code == 500
        assert (
            response.json()["error"]
            == "An unexpected error occurred. Please try again later."
        )
