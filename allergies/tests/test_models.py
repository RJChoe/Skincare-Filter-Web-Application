import pytest
from allergies.models import AllergenExposure
from allergies.constants.choices import CATEGORY_TO_ALLERGENS_MAP, CATEGORY_CONTACT, CATEGORY_FOOD


@pytest.fixture
def allergen_contact(db):
    """Fixture for contact allergen."""
    return AllergenExposure.objects.create(
        category=CATEGORY_CONTACT,
        allergen_name='sls'
    )


@pytest.fixture
def allergen_food(db):
    """Fixture for food allergen."""
    return AllergenExposure.objects.create(
        category=CATEGORY_FOOD,
        allergen_name='peanuts'
    )


@pytest.mark.django_db
class TestAllergenExposureModel:
    def test_allergen_str_representation(self, allergen_contact, allergen_food):
        assert str(allergen_contact) == "Contact - Sodium Lauryl Sulfate (SLS)"
        assert str(allergen_food) == "Food - Peanuts"

    def test_category_to_allergens_map(self):
        contact_allergens = CATEGORY_TO_ALLERGENS_MAP.get(CATEGORY_CONTACT, [])
        food_allergens = CATEGORY_TO_ALLERGENS_MAP.get(CATEGORY_FOOD, [])
        
        assert ('sls', 'Sodium Lauryl Sulfate (SLS)') in contact_allergens
        assert ('peanut', 'Peanut') in food_allergens