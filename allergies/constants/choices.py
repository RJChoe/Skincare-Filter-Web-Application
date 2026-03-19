# --- Category Definitions ---
# Category Keys (Generic Database values)
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from typing import Final, Literal

CategoryKey = Literal["food", "contact", "inhalant", "other"]
ChoiceItem = tuple[str, str]  # (value, label)
AllergyChoice = tuple[CategoryKey, str, Sequence[ChoiceItem]]

CATEGORY_FOOD: Final[CategoryKey] = "food"
CATEGORY_CONTACT: Final[CategoryKey] = "contact"
CATEGORY_INHALANT: Final[CategoryKey] = "inhalant"
CATEGORY_OTHER: Final[CategoryKey] = (
    "other"  # <-- String Value stored in DB (self.category)
)

# <-- Category label (displayed via self.get_category_display())
# --- Category Choices (For the Model field) ---
CATEGORY_CHOICES = [
    (CATEGORY_FOOD, "Food Allergens"),
    (CATEGORY_CONTACT, "Contact/Topical Allergens"),
    (CATEGORY_INHALANT, "Inhalant Allergens"),
    (CATEGORY_OTHER, "Other Allergens"),
]


# --- choices/specific allergen lists (Key-Value Pairs for the database) ---
## alphabetical ##

# Acids and exfoliants
ACID_ALLERGENS: Final[tuple[ChoiceItem, ...]] = (
    ("glycolic_acid", "Glycolic Acid"),
    ("salicylic_acid", "Salicylic Acid"),
    ("lactic_acid", "Lactic Acid"),
    ("citric_acid", "Citric Acid"),
    ("benzoic_acid", "Benzoic Acid"),
    ("sorbic_acid", "Sorbic Acid"),
)

# Botanical/Essential oils
BOTANICAL_ALLERGENS: Final[tuple[ChoiceItem, ...]] = (
    ("tea_tree_oil", "Tea Tree Oil"),
    ("lavender_oil", "Lavender Oil"),
    ("peppermint_oil", "Peppermint Oil"),
    ("eucalyptus_oil", "Eucalyptus Oil"),
    ("rose_oil", "Rose Oil"),
    ("chamomile", "Chamomile"),
    ("ylang_ylang", "Ylang Ylang"),
    ("sandalwood", "Sandalwood"),
    ("bergamot", "Bergamot Oil"),
    ("lemongrass", "Lemongrass Oil"),
)

# Colorants and dyes
COLORANT_ALLERGENS: Final[tuple[ChoiceItem, ...]] = (
    ("ci_dyes", "CI Dyes (Color Index)"),
    ("fd_c_dyes", "FD&C Dyes"),
    ("carmine", "Carmine (CI 75470)"),
    ("iron_oxides", "Iron Oxides"),
    ("mica", "Mica"),
)

# Contact/Topical Allergens (example)
CONTACT_ALLERGENS: Final[tuple[ChoiceItem, ...]] = (
    ("nickel", "Nickel"),
    ("latex", "Latex"),
    ("lanolin", "Lanolin"),
)

DUST_ALLERGENS: Final[tuple[ChoiceItem, ...]] = (
    ("dust_mite", "Dust Mite"),
    ("mold_spores", "Mold Spores"),
    ("pet_dander", "Pet Dander"),
)

FRAGRANCE_ALLERGENS: Final[tuple[ChoiceItem, ...]] = (
    # --- Original 26 (pre-2023 Annex III) ---
    ("amyl_cinnamal", "Amyl Cinnamal"),
    ("amylcinnamyl_alcohol", "Amylcinnamyl Alcohol"),
    ("anise_alcohol", "Anise Alcohol"),
    ("benzyl_alcohol", "Benzyl Alcohol"),
    ("benzyl_benzoate", "Benzyl Benzoate"),
    ("benzyl_cinnamate", "Benzyl Cinnamate"),
    ("benzyl_salicylate", "Benzyl Salicylate"),
    ("cinnamyl_alcohol", "Cinnamyl Alcohol"),
    ("cinnamal", "Cinnamal"),
    ("citral", "Citral"),
    ("citronellol", "Citronellol"),
    ("coumarin", "Coumarin"),
    ("eugenol", "Eugenol"),
    ("farnesol", "Farnesol"),
    ("geraniol", "Geraniol"),
    ("hexyl_cinnamal", "Hexyl Cinnamal"),
    ("hydroxycitronellal", "Hydroxycitronellal"),
    (
        "hydroxyisohexyl_3_cyclohexene_carboxaldehyde",
        "Hydroxyisohexyl 3-Cyclohexene Carboxaldehyde (HICC / Lyral)",
    ),
    ("isoeugenol", "Isoeugenol"),
    ("lilial", "Lilial (Butylphenyl Methylpropional)"),
    ("limonene", "Limonene"),
    ("linalool", "Linalool"),
    ("methyl_2_octynoate", "Methyl 2-Octynoate"),
    ("alpha_isomethyl_ionone", "Alpha-Isomethyl Ionone"),
    ("evernia_prunastri", "Evernia Prunastri (Oakmoss Extract)"),
    ("evernia_furfuracea", "Evernia Furfuracea (Treemoss Extract)"),
    # --- 2023 Expansion (EU 2023/1545 additions) ---
    ("acetyl_cedrene", "Acetyl Cedrene"),
    ("beta_damascenone", "Beta-Damascenone"),
    ("butyl_acetate", "Butyl Acetate"),
    ("camphene", "Camphene"),
    ("camphor", "Camphor"),
    ("carvone", "Carvone"),
    ("cedrol", "Cedrol"),
    ("cinnamaldehyde", "Cinnamaldehyde"),
    ("citronellal", "Citronellal"),
    ("cyclamen_aldehyde", "Cyclamen Aldehyde"),
    ("decyl_aldehyde", "Decyl Aldehyde"),
    ("dihydrocoumarin", "Dihydrocoumarin"),
    ("dimethyl_benzyl_carbinyl_acetate", "Dimethyl Benzyl Carbinyl Acetate"),
    ("ethylene_brassylate", "Ethylene Brassylate"),
    ("hexadecanolactone", "Hexadecanolactone"),
    ("hexyl_salicylate", "Hexyl Salicylate"),
    ("ionone", "Ionone (Alpha and Beta)"),
    ("isocyclemone_e", "Isocyclemone E"),
    ("lyratyl_acetate", "Lyratyl Acetate"),
    ("menthol", "Menthol"),
    ("methyl_ionone", "Methyl Ionone"),
    ("musk_ambrette", "Musk Ambrette"),
    ("musk_tibetene", "Musk Tibetene"),
    ("neral", "Neral"),
    ("nonadienal", "2,4-Nonadienal"),
    ("nonyl_aldehyde", "Nonyl Aldehyde"),
    ("pentadecalactone", "Pentadecalactone"),
    ("phenylacetaldehyde", "Phenylacetaldehyde"),
    ("phenoxyethanol_fragrance", "Phenoxyethanol (Fragrance Use)"),
    ("rose_ketone_4", "Rose Ketone-4 (Delta-Damascone)"),
    ("santalol", "Santalol (Alpha and Beta)"),
    ("terpineol", "Terpineol"),
    (
        "tetramethyl_acetyloctahydronaphthalenes",
        "Tetramethyl Acetyloctahydronaphthalenes (OTNE)",
    ),
    ("trimethylbenzenepropanol", "Trimethylbenzenepropanol (Majantol)"),
    ("vertofix_coeur", "Vertofix Coeur (Iso E Super)"),
)

# Food Allergens (example)
FOOD_ALLERGENS: Final[tuple[ChoiceItem, ...]] = (
    ("peanut", "Peanut"),
    ("tree_nut", "Tree Nut (General)"),
    ("gluten", "Gluten / Wheat"),
    ("dairy", "Dairy / Milk"),
    ("soy", "Soy"),
    ("shellfish", "Shellfish"),
)

# Other common allergens
OTHER_ALLERGENS: Final[tuple[ChoiceItem, ...]] = (
    ("retinol", "Retinol/Retinoids"),
    ("vitamin_c", "Vitamin C (L-Ascorbic Acid)"),
    ("niacinamide", "Niacinamide"),
    ("propylene_glycol", "Propylene Glycol"),
    ("butylene_glycol", "Butylene Glycol"),
    ("dimethicone", "Dimethicone"),
    ("tocopherol", "Tocopherol (Vitamin E)"),
    ("alcohol_denat", "Alcohol Denat"),
    ("isopropyl_alcohol", "Isopropyl Alcohol"),
)

# Pollen Allergens
POLLEN_ALLERGENS: Final[tuple[ChoiceItem, ...]] = (
    ("birch_pollen", "Birch Pollen"),
    ("chrysanthemum", "Chrysanthemum"),
    ("goldenrod", "Goldenrod"),
    ("grass_pollen", "Grass Pollen"),
    ("humulus_japonicus", "Humulus Japonicus"),
    ("lambs_quarters", "Lamb's Quarters"),
    ("mulberry", "Mulberry"),
    ("locust", "Locust"),
    ("oak_pollen", "Oak Pollen"),
    ("pine", "Pine"),
    ("plane_tree", "Plane Tree"),
    ("ragweed", "Ragweed Pollen"),
    ("rape", "Rape"),
    ("spruce", "Spruce"),
    ("tree_pollen", "Tree Pollen"),
    ("queen_palm", "Queen Palm"),
)

# Preservatives
PRESERVATIVE_ALLERGENS: Final[tuple[ChoiceItem, ...]] = (
    ("parabens", "Parabens (Methylparaben, Propylparaben, etc.)"),
    ("formaldehyde", "Formaldehyde"),
    ("formaldehyde_releasers", "Formaldehyde Releasers"),
    ("methylisothiazolinone", "Methylisothiazolinone (MI)"),
    ("methylchloroisothiazolinone", "Methylchloroisothiazolinone (MCI)"),
    ("benzalkonium_chloride", "Benzalkonium Chloride"),
    ("bronopol", "Bronopol"),
    ("iodopropynyl_butylcarbamate", "Iodopropynyl Butylcarbamate"),
)

# Proteins and extracts
PROTEIN_ALLERGENS: Final[tuple[ChoiceItem, ...]] = (
    ("collagen", "Collagen"),
    ("keratin", "Keratin"),
    ("silk_protein", "Silk Protein"),
    ("wheat_protein", "Wheat Protein"),
    ("soy_protein", "Soy Protein"),
    ("beeswax", "Beeswax"),
    ("propolis", "Propolis"),
    ("royal_jelly", "Royal Jelly"),
)

# UV filters/Sunscreen ingredients
SUNSCREEN_ALLERGENS: Final[tuple[ChoiceItem, ...]] = (
    ("oxybenzone", "Oxybenzone (Benzophenone-3)"),
    ("octinoxate", "Octinoxate (Octyl Methoxycinnamate)"),
    ("avobenzone", "Avobenzone"),
    ("octocrylene", "Octocrylene"),
    ("homosalate", "Homosalate"),
    ("titanium_dioxide", "Titanium Dioxide"),
    ("zinc_oxide", "Zinc Oxide"),
)

# Surfactants and emulsifiers
SURFACTANT_ALLERGENS: Final[tuple[ChoiceItem, ...]] = (
    ("sls", "Sodium Lauryl Sulfate (SLS)"),
    ("sles", "Sodium Laureth Sulfate (SLES)"),
    ("cocamidopropyl_betaine", "Cocamidopropyl Betaine"),
    ("peg_compounds", "PEG Compounds (Polyethylene Glycol)"),
    ("polysorbates", "Polysorbates"),
    ("sodium_lauroyl_sarcosinate", "Sodium Lauroyl Sarcosinate"),
)

# --- The Grouped Choice Constant (Grouping/UI)---
# list of 3-tuples: (database_key, human_readable_label, choice_list)
# useful django form rendering <optgroup> tags
# template iteration (require human readable category label)
# Assuming you have defined the Category Keys (GENERIC_CONTACT, etc.)
# and the Specific Allergen Lists (FRAGRANCE_ALLERGENS, etc.)

# --- Form Grouping for OptGroups (3-tuples) ---
# Structure: (category_key, optgroup_label, choices_list)
FORM_ALLERGIES_CHOICES: list[AllergyChoice] = [
    # All of these items will be classified as 'contact' in the database
    (CATEGORY_CONTACT, "Acids & Exfoliants", ACID_ALLERGENS),
    (CATEGORY_CONTACT, "Botanicals & Essential Oils", BOTANICAL_ALLERGENS),
    (CATEGORY_CONTACT, "Colorants & Dyes", COLORANT_ALLERGENS),
    (CATEGORY_CONTACT, "General Contact Allergens", CONTACT_ALLERGENS),
    (CATEGORY_CONTACT, "Cosmetic Fragrances", FRAGRANCE_ALLERGENS),
    (CATEGORY_CONTACT, "Cosmetic Preservatives", PRESERVATIVE_ALLERGENS),
    (CATEGORY_CONTACT, "Proteins & Extracts", PROTEIN_ALLERGENS),
    (CATEGORY_CONTACT, "Sunscreen Ingredients", SUNSCREEN_ALLERGENS),
    (CATEGORY_CONTACT, "Surfactants & Emulsifiers", SURFACTANT_ALLERGENS),
    # This item will be classified as 'food' in the database
    (CATEGORY_FOOD, "Major Food Allergens", FOOD_ALLERGENS),
    # This item will be classified as 'inhalant' in the database
    (CATEGORY_INHALANT, "Environmental Inhalants", DUST_ALLERGENS),
    (CATEGORY_INHALANT, "Pollen Allergens", POLLEN_ALLERGENS),
    (CATEGORY_OTHER, "Other General Contact", OTHER_ALLERGENS),
]


def _assert_allergen_tuples_well_formed(
    form_choices: Iterable[AllergyChoice],
) -> None:
    for group_index, group in enumerate(form_choices):
        if not isinstance(group, tuple) or len(group) != 3:
            raise AssertionError(
                f"Malformed group at index {group_index} in FORM_ALLERGIES_CHOICES:"
                f" expected a 3-tuple (category_key, label, choices), got {group!r}"
            )
        _, optgroup_label, choice_list = group
        for item_index, item in enumerate(choice_list):
            if (
                not isinstance(item, tuple)
                or len(item) != 2
                or not all(isinstance(s, str) for s in item)
            ):
                raise AssertionError(
                    f"Malformed entry at index {item_index} in group {optgroup_label!r}:"
                    f" expected a 2-tuple of strings (allergen_key, label), got {item!r}"
                )


def _assert_allergen_keys_unique(
    form_choices: Iterable[AllergyChoice],
) -> None:
    seen: dict[str, str] = {}  # allergen_key -> first optgroup label
    duplicates: list[str] = []

    for _, optgroup_label, choice_list in form_choices:
        for allergen_key, _ in choice_list:
            if allergen_key in seen:
                duplicates.append(
                    f"  {allergen_key!r}: first seen in {seen[allergen_key]!r},"
                    f" also in {optgroup_label!r}"
                )
            else:
                seen[allergen_key] = optgroup_label

    if duplicates:
        raise AssertionError(
            "Duplicate allergen keys detected across groups:\n" + "\n".join(duplicates)
        )


_assert_allergen_tuples_well_formed(FORM_ALLERGIES_CHOICES)
_assert_allergen_keys_unique(FORM_ALLERGIES_CHOICES)

# --- Inverse Map (Category -> Specific Choices) ---
# Maps category_key -> list of (specific_key, specific_label)


def build_category_to_allergens_map(
    form_allergies_choices: Iterable[AllergyChoice],
) -> dict[CategoryKey, list[ChoiceItem]]:
    acc: defaultdict[CategoryKey, list[ChoiceItem]] = defaultdict(list)

    for category_key, _, choice_list in form_allergies_choices:
        acc[category_key].extend(choice_list)

    return dict(acc)


CATEGORY_TO_ALLERGENS_MAP: dict[CategoryKey, list[ChoiceItem]] = (
    build_category_to_allergens_map(FORM_ALLERGIES_CHOICES)
)

# Now, CATEGORY_TO_ALLERGENS_MAP looks like:
# {
#    'contact': [
# ('glycolic_acid', 'Glycolic Acid'),
# ('tea_tree_oil', 'Tea Tree Oil'),
# ...
# ],
#    'food': [
# ('peanut', 'Peanut'),
# ('tree_nut', 'Tree Nut (General)'),
# ...
# ],
#    ...
# }


# --- Pre-calculate a flat map for efficient lookups ---
# Maps specific allergen_key -> human_readable_label across ALL categories.
def build_flat_allergen_label_map(
    category_to_allergens_map: Mapping[CategoryKey, Sequence[ChoiceItem]],
) -> dict[str, str]:
    """Creates a single dictionary mapping all allergen keys
    (e.g., 'peanut') to their labels (e.g., 'Peanut'),
    optimized for __str__ lookups.
    """
    flat_map: dict[str, str] = {}

    for allergen_list in category_to_allergens_map.values():
        flat_map.update(dict(allergen_list))

    return flat_map


# This dictionary is created once when the module is loaded.
FLAT_ALLERGEN_LABEL_MAP: dict[str, str] = build_flat_allergen_label_map(
    CATEGORY_TO_ALLERGENS_MAP
)

# FLAT_ALLERGEN_LABEL_MAP now looks like:
# {
#     'glycolic_acid': 'Glycolic Acid',
#     'tea_tree_oil': 'Tea Tree Oil',
#     'peanut': 'Peanut',
#     'linalool': 'Linalool',
#     # ... every single allergen key is mapped to its label
# }
