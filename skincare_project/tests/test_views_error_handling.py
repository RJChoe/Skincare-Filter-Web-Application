from unittest.mock import patch

import pytest
from django.urls import reverse

from allergies.services import MatchResult


@pytest.mark.django_db
class TestProductViewErrorHandling:
    """Test error handling in skincare_project product view."""

    def test_get_unauthenticated_redirects(self, client):
        response = client.get(reverse("product"))
        assert response.status_code == 302

    def test_get_authenticated_returns_200(self, authenticated_client):
        response = authenticated_client.get(reverse("product"))
        assert response.status_code == 200

    def test_post_unauthenticated_redirects(self, client):
        response = client.post(reverse("product"), {"ingredients": "water, glycerin"})
        assert response.status_code == 302

    def test_post_empty_ingredients_shows_error(self, authenticated_client):
        """Empty ingredient input renders an inline error, not a 4xx JSON response."""
        response = authenticated_client.post(reverse("product"), {"ingredients": ""})
        assert response.status_code == 200
        assert "error" in response.context
        assert response.context["error"] != ""

    def test_post_safe_result(self, authenticated_client):
        """When check_ingredients returns no matches, the template gets checked=True and empty matches."""
        with patch("skincare_project.views.check_ingredients", return_value=[]):
            response = authenticated_client.post(
                reverse("product"), {"ingredients": "water, glycerin"}
            )
        assert response.status_code == 200
        assert response.context["checked"] is True
        assert response.context["matches"] == []

    def test_post_unsafe_result(self, authenticated_client):
        """When check_ingredients returns matches, the template gets the match list."""
        match = MatchResult(
            allergen_key="nickel",
            display_label="Nickel",
            severity_level="moderate",
            is_confirmed=True,
        )
        with patch("skincare_project.views.check_ingredients", return_value=[match]):
            response = authenticated_client.post(
                reverse("product"), {"ingredients": "nickel, water"}
            )
        assert response.status_code == 200
        assert response.context["checked"] is True
        assert len(response.context["matches"]) == 1
        assert response.context["matches"][0].display_label == "Nickel"

    def test_post_unexpected_error_returns_500(self, authenticated_client):
        """Unexpected exceptions in POST handler must return 500 HTML."""
        with patch(
            "skincare_project.views.check_ingredients",
            side_effect=Exception("unexpected boom"),
        ):
            response = authenticated_client.post(
                reverse("product"), {"ingredients": "water"}
            )
        assert response.status_code == 500
        assert "error" in response.context
        assert (
            response.context["error"]
            == "An unexpected error occurred. Please try again later."
        )
