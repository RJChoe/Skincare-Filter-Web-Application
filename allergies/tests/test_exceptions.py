import pytest

from allergies.exceptions import AllergenNotFoundError, InvalidIngredientError


def test_allergen_not_found_error_is_exception():
    """AllergenNotFoundError must be a subclass of Exception."""
    assert issubclass(AllergenNotFoundError, Exception)


def test_allergen_not_found_error_preserves_message():
    """AllergenNotFoundError must carry the message string."""
    with pytest.raises(AllergenNotFoundError, match="allergen 'latex' not found"):
        raise AllergenNotFoundError("allergen 'latex' not found")


def test_invalid_ingredient_error_is_exception():
    """InvalidIngredientError must be a subclass of Exception."""
    assert issubclass(InvalidIngredientError, Exception)


def test_invalid_ingredient_error_preserves_message():
    """InvalidIngredientError must carry the message string."""
    with pytest.raises(InvalidIngredientError, match="invalid ingredient"):
        raise InvalidIngredientError("invalid ingredient")
