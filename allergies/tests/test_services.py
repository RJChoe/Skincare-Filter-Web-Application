"""Tests for allergies.services.check_ingredients."""

import pytest

from allergies.constants.compounds import CATEGORY_CONTACT
from allergies.exceptions import InvalidIngredientError
from allergies.models import Allergen, UserAllergy
from allergies.services import MatchResult, check_ingredients


@pytest.mark.django_db
class TestCheckIngredientsInvalidInput:
    """check_ingredients raises InvalidIngredientError for unparseable input."""

    def test_empty_string_raises(self, test_user):
        with pytest.raises(InvalidIngredientError):
            check_ingredients("", test_user)

    def test_whitespace_only_raises(self, test_user):
        with pytest.raises(InvalidIngredientError):
            check_ingredients("   ", test_user)

    def test_all_empty_tokens_raises(self, test_user):
        with pytest.raises(InvalidIngredientError):
            check_ingredients(",, ,", test_user)


@pytest.mark.django_db
class TestCheckIngredientsMatching:
    """check_ingredients returns correct MatchResult list for valid input."""

    def test_no_active_allergies_returns_empty(self, test_user):
        result = check_ingredients("Sodium Lauryl Sulfate", test_user)

        assert result == []

    def test_no_match_returns_empty(self, test_user, user_allergy):
        result = check_ingredients("water, glycerin", test_user)

        assert result == []

    def test_single_match(self, test_user, user_allergy, contact_allergen):
        result = check_ingredients("Sodium Lauryl Sulfate, water", test_user)

        assert len(result) == 1
        assert isinstance(result[0], MatchResult)
        assert result[0].allergen_key == "sodium_lauryl_sulfate"
        assert result[0].display_label == contact_allergen.label
        assert result[0].severity_level == "moderate"
        assert result[0].is_confirmed is True

    def test_multiple_matches(self, test_user, user_allergy, second_contact_allergen):
        UserAllergy.objects.create(user=test_user, allergen=second_contact_allergen)

        result = check_ingredients(
            "Sodium Lauryl Sulfate, methylparaben, water", test_user
        )

        assert len(result) == 2
        keys = {r.allergen_key for r in result}
        assert keys == {"sodium_lauryl_sulfate", "methylparaben"}

    def test_case_and_hyphen_normalization(self, test_user):
        allergen, _ = Allergen.objects.get_or_create(
            category=CATEGORY_CONTACT,
            allergen_key="glycolic_acid",
            defaults={"label": "Glycolic Acid", "subcategory": "Acids & Exfoliants"},
        )
        UserAllergy.objects.create(user=test_user, allergen=allergen)

        result = check_ingredients("GLYCOLIC-ACID", test_user)

        assert len(result) == 1
        assert result[0].allergen_key == "glycolic_acid"
