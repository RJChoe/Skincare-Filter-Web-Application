# ADR-001: Restructure Allergen Data Layer from Form-Driven Categories to Compound-Level Filter Architecture

**Status:** Accepted
**Date:** March 2026
**Author:** RJChoe

---

## Context

The Skincare Allergy Filter's core job is straightforward: a user pastes a product's ingredient list, and the app checks it against their personal allergen profile. The output is binary — safe or unsafe. Everything in the system exists to serve that matching operation.

The original data layer was not built around that job. It was built around how Django renders form dropdowns.

### What the original design looked like

The allergen catalog lived in `allergies/constants/choices.py`, structured as nested tuples designed for Django's `<optgroup>` form rendering:

```python
# 11 category constants — organized by allergen type, not by product use case
CATEGORY_FOOD = 'food'
CATEGORY_CONTACT = 'contact'
CATEGORY_FRAGRANCE = 'fragrance'
CATEGORY_PRESERVATIVE = 'preservative'
# ... 7 more

# Allergens as simple key-label pairs
SURFACTANT_ALLERGENS = [
    ("sls", "Sodium Lauryl Sulfate (SLS)"),
    ("parabens", "Parabens (Methylparaben, Propylparaben, etc.)"),
    ("peg_compounds", "PEG Compounds (Polyethylene Glycol)"),
]

# Combined into optgroup structure for form rendering
ALLERGIES_CHOICES = [
    (CATEGORY_FRAGRANCE, 'Fragrance Allergens', FRAGRANCE_ALLERGENS),
    (CATEGORY_CONTACT, 'Contact Allergens', CONTACT_ALLERGENS),
    # ...
]
```

The `Allergy` model (note: not yet renamed to `Allergen`) stored a free-text `name` field as both the identifier and the display value, and `common_names` as a comma-separated `TextField`:

```python
class Allergy(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.CharField(choices=CATEGORY_CHOICES, default=CATEGORY_OTHER)
    common_names = models.TextField(blank=True, null=True,
        help_text="Comma-separated list of alternative names")
```

The `UserAllergy` junction model was a bare link table — user, allergy, timestamp. No severity, no confirmation status, no source tracking.

### Why this could not support ingredient matching

Three specific failures made the original structure incompatible with the product's core use case:

**Abbreviation keys could not match real ingredient labels.** The allergen key `"sls"` cannot match `"Sodium Lauryl Sulfate"` as it appears on a product label, under any normalization strategy. The key was chosen for developer convenience, not for matching against real-world input.

**Group-level keys could not match individual compounds.** A product label lists `"Methylparaben"`, not `"Parabens"`. The key `"parabens"` is a human category, not a matchable compound. The same problem applied to `"peg_compounds"`, `"polysorbates"`, and `"formaldehyde_releasers"` — all group abstractions that no ingredient list would ever contain.

**Alternate names were trapped in unstructured text.** The `common_names` TextField stored synonyms as a comma-separated string — not queryable, not typed, not validated. The 24 parenthetical alternate names embedded in display labels (e.g., `"Tocopherol (Vitamin E)"`) were visible to users but invisible to code. An ingredient string containing `"Tocopherol"` could not programmatically resolve to the allergen displayed as `"Tocopherol (Vitamin E)"`.

### What triggered the recognition

The gap became visible during Gate 2 (logging infrastructure). While implementing structured logging for allergen operations, the mismatch between what the database stored and what the matching pipeline would need became clear. The data was shaped to answer "which category dropdown should this allergen appear in?" — not "does this ingredient string match any of the user's known allergens?"

Critically, this was caught before views or forms had been built out extensively. The model had been partially restructured (renamed to `Allergen`, `allergen_key` separated from display label, `UserAllergy` enriched with severity and metadata fields), but the constants layer — the source of truth for what compounds exist and how they are identified — was still form-driven. Continuing to build views and forms on top of a data layer that could not support the matching pipeline would have compounded the problem.

The decision was made to pause, finish the logging infrastructure so that work would carry forward, and then restructure the data layer before building any further.

---

## Decision

Restructure the allergen data layer around individual, chemically distinct compounds identified by their canonical names, with all known alternate names captured in typed, structured fields.

### Specific changes

**Replace `choices.py` with `compounds.py`.** The new module defines a `CompoundEntry` NamedTuple where each entry carries all its names in one place:

```python
class CompoundEntry(NamedTuple):
    key: str            # Canonical identifier: "sodium_lauryl_sulfate"
    inci_name: str      # INCI standard name: "Sodium Lauryl Sulfate"
    display_label: str  # UI label: "Sodium Lauryl Sulfate (SLS)"
    category: str       # Always "contact" in current catalog
    subcategory: str    # Display grouping: "Surfactants & Emulsifiers"
    common_names: tuple[str, ...]  # Alternate names for future alias resolution
    cas_number: str     # CAS Registry Number for regulatory tracking
    eu_annex_iii: bool  # EU Cosmetics Regulation listing
    regulatory_ref: str # Specific regulation reference
```

**Collapse to a single category.** The product is a skincare ingredient filter — all relevant allergens are contact/topical. The original 11 categories (food, fragrance, preservative, botanical, etc.) were reclassified: pure food allergens (peanut, shellfish) and inhalants (dust mite, pollen) were removed entirely. Food-derived skincare ingredients (almond oil, oat extract, soy protein) were retained as individual `CompoundEntry` rows under appropriate subcategories. The category axis was replaced by subcategory as the display grouping mechanism.

**Decompose group keys into individual compounds.** `"parabens"` became four entries: `methylparaben`, `propylparaben`, `butylparaben`, `ethylparaben` — each with its own INCI name, CAS number, and regulatory reference. The same decomposition was applied to `formaldehyde_releasers`, `peg_compounds`, and `polysorbates`.

**Expand abbreviation keys to canonical names.** `"sls"` became `sodium_lauryl_sulfate`. `"sles"` became `sodium_laureth_sulfate`. Keys now follow a strict rule: the name a cosmetics-literate person would use in conversation, lowercased and underscored.

**Add import-time validation.** The module asserts unique keys and well-formed entries at import time — a malformed or duplicate compound entry fails immediately rather than producing silent data corruption.

**Capture INCI names, CAS numbers, and regulatory data on every entry.** This data is not consumed at the current gate, but is structured and ready for the planned Synonym Mapper (alias-aware matching) and for regulatory tracking. INCI names and CAS numbers are verified against the EU CosIng database; INCIDecoder is used as a secondary cross-reference.

---

## Consequences

### What this enabled

**Phase 1 exact matching works immediately.** With `sodium_lauryl_sulfate` as the key and `"Sodium Lauryl Sulfate"` as the INCI name, a case-insensitive comparison between a normalized ingredient token and the allergen key produces a correct match. This was not possible with the old `"sls"` key.

**Alias data is structured for the Synonym Mapper.** The `common_names` tuple and `inci_name` field on every `CompoundEntry` contain the seed data for the planned `AllergenAlias` model. When that model ships, these values populate it directly — no manual re-entry. An in-memory `ALL_NAMES_TO_KEY` lookup can be derived from the same data for the MVP matching pipeline.

**EU regulatory data is captured per compound.** Every fragrance allergen in the EU's 2023 expansion list (Commission Implementing Regulation (EU) 2023/1545 of 27 July 2023, [EUR-Lex CELEX 32023R1545](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32023R1545)) and every Annex III-listed preservative carries its regulation reference and CAS number. This data supports future features (regulatory compliance display, region-aware filtering) without requiring a second data migration.

**The compound catalog is self-validating.** Import-time assertions catch duplicate keys, empty required fields, and key format violations before any test or server run. This prevents the silent divergence between the database and the display layer that was possible with the old static tuple approach.

### What it cost

**Architecture planning: a few days.** The `CompoundEntry` structure, the decomposition rules, the migration sequence, and the subcategory groupings were designed before any code was changed. This was deliberate — the original problem was building code before validating the data model, and the fix needed to avoid repeating that pattern.

**Code changes: modest.** The model had already been partially restructured (allergen_key separated from display, UserAllergy enriched with metadata fields) in an earlier iteration. The data layer pivot changed the constants module and its imports — not the model schema or the view layer. Views and forms had not been built out yet, so there was no UI code to throw away.

**Infrastructure work carried forward.** The logging infrastructure built during Gate 2 was intentionally completed before the pivot. Module-level loggers, admin action logging, and the logging configuration in settings all survived unchanged. The only deferred logging item — POST handler logging in `allergies/views.py` — was deferred by design, since POST handlers did not exist yet and would be built as part of Gate 4 on top of the new data layer.

### Trade-offs accepted

**~130 compounds defined in a Python file, not in the database.** The compound catalog lives in `compounds.py` as a tuple of NamedTuples. A seed migration will create corresponding `Allergen` rows in the database. This means the Python file is the source of truth during development, not the database. This is acceptable at the current catalog size and will be resolved by the seed migration, after which the database becomes the runtime source of truth and `compounds.py` becomes a reference/seed artifact.

**Single-category model limits future scope.** Collapsing to `contact` only means the tool cannot track food or inhalant allergies. This is intentional — the product is a skincare ingredient filter, and expanding scope would dilute the matching pipeline's accuracy. If scope expansion is warranted later, adding categories is an additive change that does not require restructuring the compound catalog.

---

## Alternatives Considered

### Fix `choices.py` in place

Add INCI names and CAS numbers to the existing tuple structure, keeping the multi-category and optgroup organization. Rejected because the structure was fundamentally form-shaped — nested tuples designed for `<optgroup>` rendering cannot cleanly carry per-compound metadata like CAS numbers, regulatory references, and typed alternate name lists. Retrofitting the structure would have produced a more complex and fragile module than replacing it.

### Keep multiple categories

Retain food, contact, fragrance, preservative, etc. as separate categories with the Allergen model's `category` field selecting between them. Rejected because the product's scope is skincare ingredients that contact the skin. Keeping food allergens (peanut, shellfish) and inhalants (dust mite, pollen) would generate false matches against ingredient lists that are exclusively topical products. Subcategory (fragrances, preservatives, acids, botanicals) replaced category as the display grouping axis — it organizes the same compounds without implying the tool handles non-skincare allergies.

### Store all compound metadata in the database from day one

Create database fields for INCI name, CAS number, common names, and regulatory data on the `Allergen` model and populate them via a data migration immediately. Rejected as premature. The compound data needed to stabilize (entry count, field set, naming conventions) before committing to a database schema. Defining the catalog in a Python NamedTuple allows rapid iteration — adding a field to `CompoundEntry` is a one-line change, while adding a database field requires a migration. The seed migration is planned as the next step once the catalog is stable.

---

## Lessons Learned

**Validate your data model against the product's core use case before building UI.** The original design built the data layer around form rendering — a legitimate concern, but not the product's primary job. The mismatch was only caught because the matching pipeline had not been built yet. If forms and views had been fully implemented on top of the old data layer, the pivot would have been significantly more expensive.

**Finish infrastructure before pivoting.** Completing the logging gate before restructuring the data layer meant that infrastructure work carried forward intact. Loggers, admin actions, and the logging configuration did not need to be revisited after the pivot. This was a deliberate sequencing choice: infrastructure is data-model-agnostic, so building it first creates a foundation that survives architectural changes.

**Design before coding, especially during a correction.** The original problem was building code (form-oriented data structures) before validating alignment with the product goal (ingredient matching). The pivot deliberately inverted that pattern: several days of architecture work — defining the `CompoundEntry` format, decomposition rules, naming conventions, and migration sequence — before any code was changed. This prevented a second misalignment.

**Catch misalignments early by working in gates.** The gate structure (dependencies → logging → error handling → forms) forced a sequential build that surfaced the data layer problem before views or forms existed. If all layers had been built in parallel, the cost of the pivot would have been much higher.

---

## References

These commits show the progression from the original form-driven design through the pivot to the current filter-driven architecture:

| Snapshot | File | Commit |
|----------|------|--------|
| Original form-driven constants | `allergies/constants/choices.py` | [`e41d644`](https://github.com/RJChoe/Skincare-Filter-Web-Application/blob/e41d6448360a51ce8885ae649ae71a83c1e16606/allergies/constants/choices.py) |
| Intermediate model (restructured, still importing choices.py) | `allergies/models.py` | [`fb41a0e`](https://github.com/RJChoe/Skincare-Filter-Web-Application/blob/fb41a0e9699be330bb0c55aeb3ab2b3e72782281/allergies/models.py) |
| Current filter-driven compound catalog | `allergies/constants/compounds.py` | [`9946b1b`](https://github.com/RJChoe/Skincare-Filter-Web-Application/blob/9946b1b97900fec908a56199cd1a8d3e41af435d/allergies/constants/compounds.py) |
