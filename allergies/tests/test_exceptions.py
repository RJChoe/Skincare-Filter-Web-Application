import pytest

from allergies.exceptions import (
    AllergenInactiveError,
    AllergenNotFoundError,
    AllergyError,
    InvalidIngredientError,
    UserAllergyConflictError,
)


class TestCustomExceptions:
    """Test custom exception classes."""

    def test_allergen_not_found_error(self):
        """Test AllergenNotFoundError is raised and caught correctly."""
        with pytest.raises(AllergenNotFoundError) as exc_info:
            raise AllergenNotFoundError("Allergen 'xyz' not found")

        assert "not found" in str(exc_info.value)
        assert isinstance(exc_info.value, AllergyError)

    def test_invalid_ingredient_error(self):
        """Test InvalidIngredientError with empty list."""
        with pytest.raises(InvalidIngredientError) as exc_info:
            raise InvalidIngredientError("Ingredient list cannot be empty")

        assert "empty" in str(exc_info.value)

    def test_exception_inheritance(self):
        """Verify all custom exceptions inherit from AllergyError."""
        assert issubclass(AllergenNotFoundError, AllergyError)
        assert issubclass(InvalidIngredientError, AllergyError)
        assert issubclass(UserAllergyConflictError, AllergyError)
        assert issubclass(AllergenInactiveError, AllergyError)
