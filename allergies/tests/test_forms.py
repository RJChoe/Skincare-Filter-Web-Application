"""Tests for allergies.forms: AllergenSelectForm and UserAllergyEditForm."""

from datetime import timedelta

import pytest

from allergies.constants.compounds import CATEGORY_CONTACT
from allergies.forms import AllergenSelectForm, UserAllergyEditForm
from allergies.models import Allergen


@pytest.mark.django_db
class TestAllergenSelectForm:
    def test_valid_when_allergen_selected(self, contact_allergen):
        form = AllergenSelectForm({"allergens": [contact_allergen.pk]})
        assert form.is_valid() is True

    def test_invalid_when_no_allergen_selected(self):
        form = AllergenSelectForm({})
        assert form.is_valid() is False
        assert "allergens" in form.errors

    def test_get_grouped_allergens_returns_tuples(self, contact_allergen):
        form = AllergenSelectForm()
        result = form.get_grouped_allergens()
        assert isinstance(result, list)
        assert all(
            isinstance(sub, str) and isinstance(allergens, list)
            for sub, allergens in result
        )

    def test_get_grouped_allergens_ordered_by_subcategory(
        self, contact_allergen, second_contact_allergen
    ):
        form = AllergenSelectForm()
        result = form.get_grouped_allergens()
        subcategories = [sub for sub, _ in result]
        assert subcategories == sorted(subcategories)

    def test_get_grouped_allergens_only_includes_active(self, contact_allergen):
        inactive_allergen, _ = Allergen.objects.get_or_create(
            category=CATEGORY_CONTACT,
            allergen_key="test_inactive_allergen",
            defaults={
                "label": "Test Inactive",
                "subcategory": "Test Subcategory",
                "is_active": False,
            },
        )
        # Ensure it's inactive in case it was seeded as active
        if inactive_allergen.is_active:
            inactive_allergen.is_active = False
            inactive_allergen.save()

        form = AllergenSelectForm()
        result = form.get_grouped_allergens()
        all_allergens = [a for _, group in result for a in group]
        assert inactive_allergen not in all_allergens


@pytest.mark.django_db
class TestUserAllergyEditForm:
    def test_empty_submission_is_valid(self, user_allergy):
        form = UserAllergyEditForm({}, instance=user_allergy)
        assert form.is_valid() is True

    @pytest.mark.parametrize(
        "choice", ["mild", "moderate", "severe", "life_threatening"]
    )
    def test_severity_level_accepts_valid_choices(self, user_allergy, choice):
        form = UserAllergyEditForm({"severity_level": choice}, instance=user_allergy)
        assert form.is_valid() is True

    def test_severity_level_rejects_invalid_choice(self, user_allergy):
        form = UserAllergyEditForm(
            {"severity_level": "super_severe"}, instance=user_allergy
        )
        assert form.is_valid() is False
        assert "severity_level" in form.errors

    @pytest.mark.parametrize(
        "choice",
        ["self_reported", "medical_professional", "allergy_test", "family_history"],
    )
    def test_source_info_accepts_valid_choices(self, user_allergy, choice):
        form = UserAllergyEditForm({"source_info": choice}, instance=user_allergy)
        assert form.is_valid() is True

    def test_source_info_rejects_invalid_choice(self, user_allergy):
        form = UserAllergyEditForm({"source_info": "reddit"}, instance=user_allergy)
        assert form.is_valid() is False
        assert "source_info" in form.errors

    def test_symptom_onset_date_rejects_future_date(self, user_allergy):
        from django.utils import timezone

        future = timezone.now().date() + timedelta(days=1)
        form = UserAllergyEditForm(
            {"symptom_onset_date": future.isoformat()},
            instance=user_allergy,
        )
        # _post_clean() calls instance.full_clean() → UserAllergy.clean() rejects future dates
        assert form.is_valid() is False
        assert "symptom_onset_date" in form.errors
