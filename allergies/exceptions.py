"""Custom exceptions for the allergies app."""


class AllergyError(Exception):
    """Base exception for allergy-related errors."""

    pass


class AllergenNotFoundError(AllergyError):
    """Raised when an allergen cannot be found."""

    pass


class InvalidIngredientError(AllergyError):
    """Raised when ingredient data is invalid or malformed."""

    pass


class UserAllergyConflictError(AllergyError):
    """Raised when attempting to create duplicate user allergy."""

    pass


class AllergenInactiveError(AllergyError):
    """Raised when attempting to use an inactive allergen."""

    pass
