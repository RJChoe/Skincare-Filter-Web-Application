from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError

from allergies.constants.compounds import (
    FLAT_ALLERGEN_LABEL_MAP,
)
from allergies.models import UserAllergy


@pytest.mark.django_db
class TestAllergenModel:
    """Tests for the Allergen model constants and representations."""

    def test_allergen_str_representation(self, contact_allergen):
        """Verify that __str__ returns formatted category and allergen labels."""
        # Expected for Contact:
        # Category label: 'Contact/Topical Allergens' (from CATEGORY_CHOICES)
        # Allergen label: 'Sodium Lauryl Sulfate (SLS)' (from FLAT_ALLERGEN_LABEL_MAP)
        assert (
            str(contact_allergen)
            == "Contact/Topical Allergens: Sodium Lauryl Sulfate (SLS)"
        )

    def test_flat_allergen_label_map_contains_expected_key(self):
        """Ensure FLAT_ALLERGEN_LABEL_MAP contains the expected allergen key."""
        assert "sodium_lauryl_sulfate" in FLAT_ALLERGEN_LABEL_MAP
        assert (
            FLAT_ALLERGEN_LABEL_MAP["sodium_lauryl_sulfate"]
            == "Sodium Lauryl Sulfate (SLS)"
        )

    def test_flat_allergen_label_map_is_non_empty(self):
        """FLAT_ALLERGEN_LABEL_MAP must contain more than one entry."""
        assert len(FLAT_ALLERGEN_LABEL_MAP) > 1, (
            "FLAT_ALLERGEN_LABEL_MAP is empty or too small."
        )


@pytest.mark.django_db
class TestUserAllergyModel:
    """Tests for UserAllergy model validation and constraints."""

    def test_str_representation(self, user_allergy):
        assert (
            str(user_allergy)
            == "testuser - Contact/Topical Allergens: Sodium Lauryl Sulfate (SLS)"
        )

    def test_clean_rejects_future_symptom_onset_date(self, user_allergy):
        user_allergy.symptom_onset_date = date.today() + timedelta(days=1)
        with pytest.raises(ValidationError, match="symptom_onset_date"):
            user_allergy.save()

    def test_clean_accepts_past_symptom_onset_date(self, user_allergy):
        user_allergy.symptom_onset_date = date.today() - timedelta(days=1)
        user_allergy.save()  # should not raise

    def test_clean_rejects_unknown_user_reaction_details_keys(self, user_allergy):
        user_allergy.user_reaction_details = {"bad_key": "value"}
        with pytest.raises(ValidationError, match="user_reaction_details"):
            user_allergy.save()

    def test_clean_accepts_valid_user_reaction_details_keys(self, user_allergy):
        user_allergy.user_reaction_details = {
            "symptom": "rash",
            "severity": "mild",
            "date": "2024-01-01",
        }
        user_allergy.save()  # should not raise

    def test_clean_rejects_unknown_admin_notes_keys(self, user_allergy):
        user_allergy.admin_notes = {"random": "val"}
        with pytest.raises(ValidationError, match="admin_notes"):
            user_allergy.save()

    def test_clean_accepts_valid_admin_notes_keys(self, user_allergy):
        user_allergy.admin_notes = {
            "verified_by": "dr_smith",
            "verification_date": "2024-01-01",
        }
        user_allergy.save()  # should not raise

    def test_unique_constraint_prevents_duplicate_user_allergen(
        self, test_user, contact_allergen, user_allergy
    ):
        # save() calls full_clean() → validate_unique() before hitting the DB,
        # so the unique constraint raises ValidationError (not IntegrityError)
        with pytest.raises(ValidationError, match="already exists"):
            UserAllergy.objects.create(user=test_user, allergen=contact_allergen)
