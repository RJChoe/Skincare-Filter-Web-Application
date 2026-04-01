import pytest

from allergies.constants.compounds import (
    FLAT_ALLERGEN_LABEL_MAP,
)


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


# TODO :
# create tests for UserAllergy model linking users to allergens
