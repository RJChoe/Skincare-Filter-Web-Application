"""Tests for allergies views: allergy_list, create_allergies, edit_allergy, delete_allergy."""

import pytest
from django.urls import reverse

from allergies.models import UserAllergy


@pytest.mark.django_db
class TestAllergyListView:
    def test_unauthenticated_get_redirects_to_login(self, client):
        response = client.get(reverse("allergies:list"))
        assert response.status_code == 302
        assert "/login/" in response["Location"]

    def test_authenticated_get_renders_correct_template(self, authenticated_client):
        response = authenticated_client.get(reverse("allergies:list"))
        assert response.status_code == 200
        assert "allergies/allergies_list.html" in [t.name for t in response.templates]


@pytest.mark.django_db
class TestCreateAllergiesView:
    def test_authenticated_post_valid_creates_user_allergies(
        self, authenticated_client, test_user, contact_allergen
    ):
        url = reverse("allergies:create")
        response = authenticated_client.post(url, {"allergens": [contact_allergen.pk]})
        assert response.status_code == 302
        assert response["Location"] == reverse("allergies:list")
        assert UserAllergy.objects.filter(
            user=test_user, allergen=contact_allergen
        ).exists()

    def test_authenticated_post_invalid_form_redirects_with_error(
        self, authenticated_client, test_user
    ):
        initial_count = UserAllergy.objects.filter(user=test_user).count()
        url = reverse("allergies:create")
        response = authenticated_client.post(url, {})
        assert response.status_code == 302
        assert response["Location"] == reverse("allergies:list")
        assert UserAllergy.objects.filter(user=test_user).count() == initial_count

    def test_unauthenticated_post_redirects_to_login(self, client, contact_allergen):
        url = reverse("allergies:create")
        response = client.post(url, {"allergens": [contact_allergen.pk]})
        assert response.status_code == 302
        assert "/login/" in response["Location"]

    def test_already_in_profile_allergen_not_duplicated(
        self, authenticated_client, test_user, contact_allergen, user_allergy
    ):
        url = reverse("allergies:create")
        response = authenticated_client.post(url, {"allergens": [contact_allergen.pk]})
        assert response.status_code == 302
        assert (
            UserAllergy.objects.filter(
                user=test_user, allergen=contact_allergen
            ).count()
            == 1
        )

    def test_batch_creation_of_multiple_allergens(
        self,
        authenticated_client,
        test_user,
        contact_allergen,
        second_contact_allergen,
    ):
        url = reverse("allergies:create")
        response = authenticated_client.post(
            url,
            {"allergens": [contact_allergen.pk, second_contact_allergen.pk]},
        )
        assert response.status_code == 302
        assert UserAllergy.objects.filter(
            user=test_user, allergen=contact_allergen
        ).exists()
        assert UserAllergy.objects.filter(
            user=test_user, allergen=second_contact_allergen
        ).exists()

    def test_post_logging_includes_pk_not_email(
        self,
        authenticated_client,
        test_user,
        contact_allergen,
        caplog,
        enable_allergies_logging,
    ):
        url = reverse("allergies:create")
        with caplog.at_level("INFO", logger="allergies.views"):
            authenticated_client.post(url, {"allergens": [contact_allergen.pk]})
        assert str(test_user.pk) in caplog.text
        assert test_user.email not in caplog.text


@pytest.mark.django_db
class TestEditAllergyView:
    def test_edit_view_get_renders_form_for_correct_user_allergy(
        self, authenticated_client, user_allergy
    ):
        url = reverse("allergies:edit", kwargs={"pk": user_allergy.pk})
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert "allergies/edit_allergy.html" in [t.name for t in response.templates]
        assert response.context["user_allergy"] == user_allergy

    def test_edit_view_post_valid_data_updates_row(
        self, authenticated_client, user_allergy
    ):
        url = reverse("allergies:edit", kwargs={"pk": user_allergy.pk})
        response = authenticated_client.post(url, {"severity_level": "severe"})
        assert response.status_code == 302
        user_allergy.refresh_from_db()
        assert user_allergy.severity_level == "severe"

    def test_edit_view_post_invalid_form_returns_form_errors(
        self, authenticated_client, user_allergy
    ):
        url = reverse("allergies:edit", kwargs={"pk": user_allergy.pk})
        response = authenticated_client.post(url, {"severity_level": "not_real"})
        assert response.status_code == 200
        assert "allergies/edit_allergy.html" in [t.name for t in response.templates]
        assert "form" in response.context
        assert response.context["form"].errors

    def test_unauthenticated_get_redirects_to_login(self, client, user_allergy):
        url = reverse("allergies:edit", kwargs={"pk": user_allergy.pk})
        response = client.get(url)
        assert response.status_code == 302
        assert "/login/" in response["Location"]

    def test_post_logging_includes_pk_not_email(
        self,
        authenticated_client,
        test_user,
        user_allergy,
        caplog,
        enable_allergies_logging,
    ):
        url = reverse("allergies:edit", kwargs={"pk": user_allergy.pk})
        with caplog.at_level("INFO", logger="allergies.views"):
            authenticated_client.post(url, {"severity_level": "severe"})
        assert str(test_user.pk) in caplog.text
        assert str(user_allergy.pk) in caplog.text
        assert test_user.email not in caplog.text


@pytest.mark.django_db
class TestDeleteAllergyView:
    def test_delete_view_post_removes_user_allergy(
        self, authenticated_client, user_allergy
    ):
        pk = user_allergy.pk
        url = reverse("allergies:delete", kwargs={"pk": pk})
        response = authenticated_client.post(url)
        assert response.status_code == 302
        assert not UserAllergy.objects.filter(pk=pk).exists()

    def test_delete_view_rejects_get_requests(self, authenticated_client, user_allergy):
        url = reverse("allergies:delete", kwargs={"pk": user_allergy.pk})
        response = authenticated_client.get(url)
        assert response.status_code == 405

    def test_unauthenticated_post_redirects_to_login(self, client, user_allergy):
        url = reverse("allergies:delete", kwargs={"pk": user_allergy.pk})
        response = client.post(url)
        assert response.status_code == 302
        assert "/login/" in response["Location"]

    def test_post_logging_includes_pk_not_email(
        self,
        authenticated_client,
        test_user,
        user_allergy,
        caplog,
        enable_allergies_logging,
    ):
        url = reverse("allergies:delete", kwargs={"pk": user_allergy.pk})
        with caplog.at_level("INFO", logger="allergies.views"):
            authenticated_client.post(url)
        assert str(test_user.pk) in caplog.text
        assert str(user_allergy.pk) in caplog.text
        assert test_user.email not in caplog.text
