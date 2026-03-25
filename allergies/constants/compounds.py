# allergies/constants/compounds.py

from typing import NamedTuple


class CompoundEntry(NamedTuple):
    """A single allergen/ingredient compound with all known identifiers.

    This is the seed data source. Each entry becomes one Allergen row.
    The names list becomes AllergenAlias rows when Phase 2 ships.
    """

    key: str  # Canonical ID: INCI-normalized, lowercase, underscored
    inci_name: str  # Official INCI name (primary matching target)
    display_label: str  # Clean human-readable label (no parens, no aliases)
    category: str  # DB category value: 'contact', 'food'
    subcategory: str  # Optgroup label for form rendering
    common_names: tuple[str, ...] = ()  # Trade names, abbreviations, common names
    cas_number: str = ""  # CAS registry number (empty if not applicable)
    eu_annex_iii: bool = False  # True if listed in EU Cosmetics Regulation Annex III
    regulatory_ref: str = ""  # e.g. "EU 2023/1545" or "26 original"
