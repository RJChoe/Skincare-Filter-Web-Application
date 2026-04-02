"""Ingredient-checking service for the allergies app.

Public API:
    check_ingredients(ingredient_text, user) -> list[MatchResult]
"""

import logging
from typing import NamedTuple

from allergies.exceptions import InvalidIngredientError
from allergies.models import UserAllergy
from users.models import CustomUser

logger = logging.getLogger(__name__)


class MatchResult(NamedTuple):
    allergen_key: str  # stable DB key, e.g. "sodium_lauryl_sulfate"
    display_label: (
        str  # allergen.label with allergen_key fallback (mirrors Allergen.__str__)
    )
    severity_level: str  # "" if not set; from UserAllergy.SeverityLevel
    is_confirmed: bool  # whether clinically confirmed


def _normalize_token(token: str) -> str:
    """Normalize a single ingredient token to allergen_key format."""
    return token.strip().lower().replace("-", "_").replace(" ", "_")


def check_ingredients(
    ingredient_text: str,
    user: CustomUser,
) -> list[MatchResult]:
    """Check a comma-separated ingredient string against the user's active allergies.

    Args:
        ingredient_text: Raw comma-separated ingredient list from user input.
        user: Authenticated CustomUser instance.

    Returns:
        List of MatchResult for every allergen found in the ingredient list.
        Empty list means no allergens were found (not an error).

    Raises:
        InvalidIngredientError: If ingredient_text is blank or contains no
            parseable tokens after normalization.
    """
    stripped = ingredient_text.strip()
    if not stripped:
        logger.warning(f"check_ingredients: empty ingredient_text from user={user.pk}")
        raise InvalidIngredientError("Ingredient list cannot be empty")

    tokens: set[str] = set()
    for raw_token in stripped.split(","):
        normalized = _normalize_token(raw_token)
        if normalized:
            tokens.add(normalized)

    if not tokens:
        logger.warning(
            f"check_ingredients: no parseable tokens after normalization "
            f"for user={user.pk}"
        )
        raise InvalidIngredientError(
            "Ingredient list contains no parseable ingredients"
        )

    logger.info(f"check_ingredients: user={user.pk}, token_count={len(tokens)}")

    user_allergies = UserAllergy.objects.filter(
        user=user, is_active=True
    ).select_related("allergen")

    matches: list[MatchResult] = []
    for ua in user_allergies:
        if ua.allergen.allergen_key in tokens:
            logger.info(
                f"check_ingredients: match found — "
                f"user={user.pk}, allergen_key={ua.allergen.allergen_key}, "
                f"severity={ua.severity_level}"
            )
            matches.append(
                MatchResult(
                    allergen_key=ua.allergen.allergen_key,
                    display_label=ua.allergen.label or ua.allergen.allergen_key,
                    severity_level=ua.severity_level,
                    is_confirmed=ua.is_confirmed,
                )
            )

    logger.info(
        f"check_ingredients: complete — "
        f"user={user.pk}, matches={len(matches)}/{len(tokens)} tokens"
    )
    return matches
