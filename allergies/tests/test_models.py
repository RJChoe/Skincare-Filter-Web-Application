import pytest

from allergies.constants.choices import (
    CATEGORY_CONTACT,
    CATEGORY_FOOD,
    CATEGORY_TO_ALLERGENS_MAP,
)
from allergies.models import Allergen


@pytest.fixture
def allergen_contact(db):
    """Fixture for contact allergen.

    Assumes 'sls' key maps to 'Sodium Lauryl Sulfate (SLS)' label.
    """
    return Allergen.objects.create(category=CATEGORY_CONTACT, allergen_key="sls")


@pytest.fixture
def allergen_food(db):
    """Fixture for food allergen. Using 'peanut' to match constant test."""
    return Allergen.objects.create(category=CATEGORY_FOOD, allergen_key="peanut")


class TestAllergenModel:
    # Assumption: The AllergenExposure.__str__ method is implemented like this:
    # def __str__(self):
    #     return f"{self.get_category_display()} - {self.get_allergen_name_display()}"

    def test_allergen_str_representation(self, allergen_contact, allergen_food):
        # Expected for Contact:
        # Category label: 'Contact/Topical Allergens' (from CATEGORY_CHOICES)
        # Allergen label: 'Sodium Lauryl Sulfate (SLS)'
        # (from SURFACTANT_ALLERGENS)
        assert (
            str(allergen_contact)
            == "Contact/Topical Allergens: Sodium Lauryl Sulfate (SLS)"
        )

        # Expected for Food:
        # Category label: 'Food Allergens' (from CATEGORY_CHOICES)
        # Allergen label: 'Peanut' (from FOOD_ALLERGENS)
        assert str(allergen_food) == "Food Allergens: Peanut"

    # No model instances are needed for this test, as it only checks constants
    def test_category_to_allergens_map(self):
        # CATEGORY_TO_ALLERGENS_MAP should contain all specific choices under the key
        contact_allergens = CATEGORY_TO_ALLERGENS_MAP.get(CATEGORY_CONTACT, [])
        food_allergens = CATEGORY_TO_ALLERGENS_MAP.get(CATEGORY_FOOD, [])

        # These assertions check if the keys and labels are correctly
        # packed into the map
        assert ("sls", "Sodium Lauryl Sulfate (SLS)") in contact_allergens
        assert ("peanut", "Peanut") in food_allergens

        # Ensure the list is not empty
        assert len(contact_allergens) > 1, (
            "Contact allergens map is empty or too small."
        )
        assert len(food_allergens) > 1, "Food allergens map is empty or too small."


# TODO :
# create tests for UserAllergy model linking users to allergens

# Add more tests for edge cases, such as invalid category/allergen combinations,
# uniqueness constraints, and inactive allergens if needed.
