# Project Status — Skincare Allergy Filter

> **This is the only file that changes after each work session.**
> Update it when a task is finished, a gap is discovered, or a gate is completed.
> Do not embed status in `copilot-instructions.md` — keep that file stable.

---

## Gate Summary

| Gate | Name | Status |
|------|------|--------|
| 1 | Dependencies | ✅ Complete |
| 2 | Logging Infrastructure | 🚧 In Progress (waiting on POST handler Gate 4) |
| 3 | Error Handling | ✅ Complete |
| 4 | Forms & Validation | ❌ Not started |
| 5 | Tests | ❌ Not started |

---

## Gate Detail

### Gate 1: Dependencies — ✅ Complete
- ✅ `django-environ` installed and in `pyproject.toml`
- ✅ Verified working in `skincare_project/settings.py`
- ✅ `uv.lock` synced and committed

### Gate 2: Logging Infrastructure — 🚧 In Progress

**Complete when:** every view function and admin action file has a module-level
logger, and all CREATE / UPDATE / DELETE events log at INFO; errors log at ERROR
with `exc_info=True`.

| File | Status | Notes |
|------|--------|-------|
| `allergies/admin.py` | ✅ Complete | present — all 4 actions logged correctly |
| `allergies/views.py` | ⏳ Deferred to Gate 4 | GET access logged. CREATE/UPDATE/DELETE logging requires the POST handler — will be completed as part of Gate 4, not before it |
| `skincare_project/views.py` | ✅ Complete | present — product POST handler partially stubbed with correct logging |
| `skincare_project/settings.py` LOGGING config | ✅ Complete | Existence confirmed from source |

### Gate 3: Error Handling — ✅ Complete

**Complete when:** all view functions have `try/except` with user-friendly error
rendering, `@transaction.atomic` on all writes, and `allergies/exceptions.py`
exists with domain exception classes.

| Item | Status | Notes |
|------|--------|-------|
| `try/except` in `allergies/views.py` | ✅ Complete | Implemented |
| `try/except` in `skincare_project/views.py` | ✅ Complete | Implemented |
| `@transaction.atomic` on multi-model writes | ✅ Complete | File exists |
| `allergies/exceptions.py` | ✅ Complete | File exists |
| `AllergenNotFoundError` class | ✅ Complete | Class exists |
| `InvalidIngredientError` class | ✅ Complete | Class exists |
| Validation errors surfaced (no 500s) | ✅ Complete | Confirmed from source |

### Gate 4: Forms & Validation — ❌ Blocked

**No hard blockers.** Gates 2 and 3 are effectively unblocked — the only open Gate 2 item (`allergies/views.py` POST logging) resolves within this gate, not before it.

Pre-Gate 4 Tasks (data foundation):
0. ✅ Complete: Complete `allergies/constants/compounds.py` — all `CompoundEntry`
   rows migrated from `choices.py`; no stubs
  - Create CompoundEntry NamedTuple with fields: key, inci_name, display_label, category, subcategory, common_names, cas_number, eu_annex_iii, regulatory_ref
  - Migrate every entry from choices.py to CompoundEntry rows, applying locked decisions:
      - All entries get category="contact"
      - Remove pure food allergens (peanut, shellfish) and inhalants (dust mite, pollen, pet dander)
      - Add food-derived skincare ingredients as individual compounds with subcategory="Food-Derived Ingredients" (albumin, hydrolyzed wheat protein, almond oil, coconut oil, oat extract, soy protein, etc.)
      - Decompose group-level keys: parabens → methylparaben, propylparaben, butylparaben, ethylparaben; same for formaldehyde_releasers, peg_compounds, polysorbates
      - Expand abbreviation keys: sls → sodium_lauryl_sulfate, sles → sodium_laureth_sulfate
      - Populate inci_name and common_names on every entry (data captured for future Synonym Mapper, not consumed at Gate 4)
      - Set eu_annex_iii and regulatory_ref on fragrance and preservative entries
  - Export: COMPOUNDS, CompoundEntry, FLAT_ALLERGEN_LABEL_MAP, CATEGORY_CHOICES (single entry), CATEGORY_CONTACT
  - Do not export: FORM_ALLERGIES_CHOICES, INCI_NAME_TO_KEY, ALL_NAMES_TO_KEY, CATEGORY_TO_ALLERGENS_MAP
  - Import-time validation: assert unique keys, assert well-formed entries
  - No imports from choices.py

0b. 🚧 In Progress: Delete choices.py, update all imports
  - Update imports in models.py, conftest.py, views.py to point to allergies.constants.compounds
  - Remove CATEGORY_OTHER, CATEGORY_FOOD, CATEGORY_INHALANT from all files
  - Update conftest.py: remove food_allergen fixture, replace with a second contact-category fixture, expand allergen_key="sls" to "sodium_lauryl_sulfate", add label= and subcategory= to .create() calls once those fields exist
  - Delete allergies/constants/choices.py
  - Run existing tests — they should pass with import path and fixture key updates

0c. Run Migration 1 (schema): add `label` field to `Allergen` — `makemigrations` output only,
    no data writes, no behavior change (see Active Work Items for full sequence)
  - uv run python manage.py makemigrations allergies --name add_label_and_subcategory_fields
  - Adds label = CharField(max_length=200, blank=False, default="") to Allergen
  - Adds subcategory = CharField(max_length=100, blank=False, default="") to Allergen
  - Updates category field: default=CATEGORY_CONTACT (was CATEGORY_OTHER)
  - Pure AddField operations — no RunPython, no data writes
  - Rollback is clean RemoveField with no data loss

0d. Run Migration 2 (data/seed): `RunPython` reads `ALL_COMPOUNDS`, creates `Allergen`
    rows, populates `label` on every row — depends on Migration 1
  - Hand-write allergies/migrations/XXXX_seed_allergen_catalog.py with RunPython
  - Dependencies must point to Migration 1
  - Reads COMPOUNDS from allergies.constants.compounds
  - Creates Allergen rows with category, allergen_key, label, subcategory, is_active=True
  - Provide reverse function that deletes seeded rows

0e. Immediately after both migrations land (same PR): update `Allergen.__str__()` to use
    `self.label`, delete `allergen_label` property, remove `FLAT_ALLERGEN_LABEL_MAP`
    import from `models.py`
  - Update Allergen.__str__(): replace FLAT_ALLERGEN_LABEL_MAP.get(...) with self.label
  - Delete the allergen_label property
  - Remove FLAT_ALLERGEN_LABEL_MAP import from models.py
  - After this step, models.py has zero runtime dependency on compounds.py

Gate 4 Proper Tasks (forms, views, matching):
1. Create `allergies/forms.py`
  - AllergenSelectForm: batch allergen selection
    - ModelMultipleChoiceField with CheckboxSelectMultiple widget
    - queryset=Allergen.objects.filter(is_active=True).order_by('subcategory', 'label')
    - Template groups checkboxes by subcategory

  - UserAllergyEditForm: individual allergy detail editing
    - ModelForm for UserAllergy
    - Fields: severity_level, is_confirmed, source_info, symptom_onset_date, user_reaction_details
    - All fields optional (visible but not required)

2. Create allergen profile views in allergies/views.py
  - create_allergies view (POST): receives checked allergen IDs, creates UserAllergy rows with defaults, redirects to profile list
  - edit_allergy view (GET/POST): renders and processes UserAllergyEditForm for a single UserAllergy
  - delete_allergy view (POST): removes a UserAllergy entry
  - allergy_list view (GET): displays user's current allergen profile
  - All views: @login_required, @transaction.atomic on writes, logging at INFO for create/update/delete
  - This completes the deferred Gate 2 item (POST logging in allergies/views.py)

3. Create allergies/services.py (matching pipeline)
  - check_ingredients(ingredient_text: str, user: CustomUser) -> list[MatchResult]
  - Sanitize input: remove special characters, formatting
  - Tokenize: split on commas
  - Normalize: lowercase, strip whitespace
  - Query user's active allergens: UserAllergy.objects.filter(user=user, is_active=True).select_related('allergen')
  - Compare each normalized token against each allergen.allergen_key
  - Collect all matches (do not fail-fast at the service layer)
  - Return list of matches, each including the allergen key, label, and severity level from UserAllergy

4. Create product check view in skincare_project/views.py
  - product_check view (GET): renders form with <textarea> for ingredient list
  - product_check view (POST): calls check_ingredients(), renders result
  - MVP template: if matches list is empty → "Safe"; if not empty → "Unsafe — contains: [list of matched ingredient labels]"
  - @login_required, logging at INFO

5. Create/update templates
  - Allergen selection template: grouped checkboxes by subcategory, {% csrf_token %}
  - Allergen edit template: individual detail form, {% csrf_token %}
  - Allergen list template: user's profile with edit/delete links per entry
  - Product check template: <textarea> input form + result display
  - All templates extend layout.html

6. Wire URL routes
  - Add allergen profile URLs to allergies/urls.py (create, edit, delete, list)
  - Add product check URL to skincare_project/urls.py or appropriate location
  - Ensure allergies/urls.py is included in root URL config (STATUS.md notes users/urls.py is not yet included — verify allergies/urls.py is)

7. Write tests (80% coverage for new code)
  - Test AllergenSelectForm and UserAllergyEditForm validation
  - Test check_ingredients() service function: exact match, no match, multiple matches, case insensitivity, whitespace handling
  - Test allergen profile views: GET, POST, auth redirect, error cases
  - Test product check view: GET, POST with safe result, POST with unsafe result, empty input
  - Test batch creation of UserAllergy rows from checkbox form
  - Complete Gate 2: confirm all POST handlers have INFO logging

8. Gate completion verification
  - Run uv run pytest --cov --cov-report=term-missing — 80% coverage on new code
  - Run uv run ruff check . --fix && uv run ruff format .
  - Run uv run mypy .
  - Verify complete user flow works end-to-end: create account → select allergens → paste ingredients → see result
  - Update STATUS.md: mark Gate 2 complete, mark Gate 4 complete

### Gate 5: Tests — ❌ Blocked

**No hard blockers.** Run in parallel with Gate 4.

Tasks:
1. Complete `allergies/tests/test_models.py` — TODO at L68 covers `UserAllergy`
   fields: `severity_level`, `is_confirmed`, `user_reaction_details` JSONField
   key validation, future `symptom_onset_date` rejection
2. Verify scope of `users/tests.py` (382 lines) — confirm what is and isn't covered
3. Add view tests for `allergies/views.py` (GET, POST, auth redirect, error cases)
4. Verify `allergies/tests/test_views.py` and `test_admin_error_handling.py` exist
   and pass
5. Add one `@pytest.mark.integration` test for the full allergy profile → product
   check flow
6. Meet 75% overall coverage threshold (rises to 80% at Gate 5 completion)

---

## Active Work Items

These are the specific tasks to complete **right now**, in order:

### Pre-Gate 4 Tasks (data foundation) — start here

See Gate 4 Detail above — start with Pre-Gate 4 Task 0b (compounds.py).

---

## Known Gaps (Exist but Incomplete)

| Item | What Exists | What's Missing |
|------|-------------|----------------|
| `allergies/constants/choices.py` | Architecture in progress; map/lookup functions solid | `compounds.py` migration in progress — `ALL_COMPOUNDS` tuple being built. Two-migration sequence (schema then seed) not yet written. `choices.py` will be **deleted** after the seed migration lands — not split. `compounds.py` holds the canonical tuple only; no lookup tables at Gate 4. |
| `allergies/models.py` | `Allergen` and `UserAllergy` models; JSONField key validation in `clean()` | Unverified against actual file on disk — confirm matches uploaded version |
| `allergies/views.py` | Error handling implemented; GET logging implemented | CREATE/UPDATE/DELETE logging and POST logic blocked until Gate 4 |
| `skincare_project/views.py` | Logging complete; `home` and `product` GET views exist | `product` POST handler not implemented (Gate 4) |
| `allergies/tests/test_models.py` | Some `Allergen` tests exist | `UserAllergy` tests missing — confirmed TODO at L59 |
| `users/tests.py` | 382 lines exist | Scope of coverage unknown — audit required |
| `allergies/constants/choices.py` display maps | `FLAT_ALLERGEN_LABEL_MAP` and `CATEGORY_TO_ALLERGENS_MAP` are built from static tuples at import time | Any allergen added via the admin panel won't appear in these maps — silent divergence between DB and display layer. Acceptable while admin is seed-only. This file is slated for deletion after the seed migration lands; these maps go with it. |
| `ChoiceItem` type alias in `choices.py` | Defined as `tuple[str, str]` | Moot — disappears when `choices.py` is deleted. No fix needed. |

---

## Blocked Features

These cannot be started until the gates above are done:

- 🚫 **User-facing allergy forms** — needs Gate 4 (forms)

---

## Planned (Post-Gates, Not Started)

- **Synonym Mapper / `AllergenAlias` model** — Replaces exact-string matching with alias-aware resolution. A many-to-one table maps every known surface form of an ingredient (INCI name, common name, abbreviation) to a canonical allergen_key, so "Benzophenone-3" and "Oxybenzone" resolve to the same allergen record. No model, migration, or design document exists yet. The seed data is already captured: CompoundEntry.inci_name and CompoundEntry.common_names in compounds.py contain the alias data that will populate AllergenAlias rows. The matching pipeline in allergies/services.py is the integration point — alias resolution changes the lookup function, not the pipeline structure. Two implementation paths: (1) in-memory lookup tables built from compounds.py (fast to ship, sufficient for ~200 compounds), or (2) AllergenAlias Django model with database lookups (required if the alias catalog grows beyond what a Python dict should hold). Either path is a change to services.py only — no form, view, or template changes required.

- **Severity-aware result display** — Upgrades the product check from binary safe/unsafe to severity-differentiated output. Matches with severity_level="severe" or "life_threatening" render as blocks; matches with "mild" or "moderate" render as warnings. The matching pipeline in allergies/services.py already collects all matches with their severity — this is a template-only change. Replace the binary result template with one that groups matches by severity and renders them differently. No model, form, view logic, or pipeline changes required.

- **Product lookup** — A second input method alongside text paste. The user searches for a product by name instead of pasting an ingredient list. Requires a product database (either sourced from an external dataset or built via an external API integration such as Open Beauty Facts). The matching pipeline is unchanged — product lookup resolves a product name to an ingredient string, which feeds the same check_ingredients() function in allergies/services.py. This is an input method, not a matching change. Text paste remains available as a fallback for products not in the database.

---

## Compound Catalog Design Decisions

Decisions recorded here govern the structure of `allergies/constants/compounds.py`.
They are intentional and should not be "fixed" without revisiting the rationale.

### Reference source

All INCI names and CAS numbers in the catalog are verified against the EU CosIng
(Cosmetic Ingredient) database maintained by the European Commission:
https://ec.europa.eu/growth/tools-databases/cosing/

INCIDecoder (incidecoder.com) is used as a secondary cross-reference to confirm
which INCI names appear on real product labels. See the module docstring in
`compounds.py` for the full reference policy.

### One CompoundEntry per chemically distinct substance

The compound catalog is a chemistry-level data layer. Each entry represents one
CAS-distinct substance with one primary INCI name. When multiple substances share
an allergen concern for users (e.g. "soy"), they remain separate entries in the
catalog. User-facing grouping is the responsibility of the planned AllergenAlias /
Synonym Mapper layer, not the compound catalog.

Merging entries that have different CAS numbers destroys information that may matter
for regulatory tracking (eu_annex_iii, regulatory_ref) and for future integrations
with external ingredient databases that key on CAS.

### Soy: soy_protein + soy_extract kept as two entries

- `soy_protein` (Hydrolyzed Soy Protein, CAS 68607-88-5) — subcategory Proteins & Extracts
- `soy_extract` (Glycine Soja Extract, CAS 84776-91-0) — subcategory Food-Derived Ingredients

Different CAS numbers, different INCI names, different manufacturing processes.
Both are soy-derived and both matter to a user with a soy allergy. At Gate 4 MVP,
both appear as separate checkboxes — display labels are distinct enough that users
can identify and select both. When the AllergenAlias layer ships, a single "Soy"
user-facing group will resolve to both allergen_keys.

Note: the original soy_extract entry carried CAS 68153-28-6, which does not appear
in CosIng or any INCI reference database. CosIng lists Glycine Soja Extract under
CAS 84776-91-0 (CosIng Ref 34118). Corrected during Pre-Gate 4 data review.

### Soy oil (Glycine Soja Oil) intentionally excluded

Glycine Soja Oil (soybean oil, CAS 8001-22-7) is a CosIng-registered INCI name
and is soy-derived, but it is not included in the catalog. Refined soybean oil has
nearly all protein removed during processing and is generally considered
non-allergenic for topical use. The CIR Expert Panel reviewed soy-derived cosmetic
ingredients and concluded that skin reactions from cosmetic soy proteins were
unlikely; soybean oil is even further removed from the allergenic protein fraction.

Including it would generate false positives — a user with a soy contact allergy
would see "UNSAFE" on products containing soybean oil that are almost certainly
safe for them. For a safety-oriented tool, false positives erode trust.

If future evidence or user demand warrants it, soybean oil can be added as either:
(a) its own CompoundEntry, or (b) a tiered alias group in the AllergenAlias layer
(e.g. "Soy — strict" vs "Soy — all derivatives including oil"). That is a UX
decision for the alias layer, not a compound catalog decision.

### Lemongrass: single entry, most common INCI as primary

CosIng registers three valid Cymbopogon species as lemongrass-type oils, all sharing
the generic CAS 8007-02-1:

- Cymbopogon Citratus Leaf Oil (West Indian lemongrass) — most common on product labels
- Cymbopogon Flexuosus Oil (East Indian lemongrass) — second most common
- Cymbopogon Schoenanthus Oil (camel grass) — least common, but valid in CosIng

Because all three share the same CAS and represent the same allergen concern, the
catalog carries a single `lemongrass_oil` entry with `inci_name="Cymbopogon Citratus
Leaf Oil"` (the most frequently encountered form). The other two species names are
stored in `common_names` for future alias resolution. If a future regulatory or
chemical distinction emerges between species, split into separate entries at that time.

Note: the original entry used `inci_name="Cymbopogon Schoenanthus Oil"`, which is
valid in CosIng but is the least common of the three on product labels. Corrected
during Pre-Gate 4 data review to maximize matching coverage at the MVP stage.

---

## Verification Protocol

Before marking any gate ✅ Complete in this file:

1. Open the actual source file — do not rely on this document's prior claims
2. Confirm the specific lines exist: e.g. `grep -n "getLogger" allergies/views.py`
3. Run `uv run pytest` and confirm no related tests fail
4. Update this file — not `copilot-instructions.md`

**Do not mark a gate complete based on documentation alone.**

---

⚠️ Project knowledge intentionally excludes views.py, settings.py,
and test files — attach per-chat as needed for relevant tasks.

---
*Last updated: 3/27/2026 10:25 PM — updated collision on common names damascenone. Created compounds.py and updated SATTUS.md with design decisions on multiple INCI common names*
