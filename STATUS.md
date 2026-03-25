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

Tasks:
0. Complete `allergies/constants/compounds.py` — all `CompoundEntry`
   rows migrated from `choices.py`; no stubs
0b. Write seed migration `allergies/migrations/XXXX_seed_allergen_catalog`
    — reads from `ALL_COMPOUNDS`, populates `Allergen` table;
    `Allergen.__str__` switches to `self.label` after this lands
1. Create `allergies/forms.py` with `UserAllergyForm`
2. Implement dynamic `allergen_key` filtering (category → allergen cascading)
3. Add `{% csrf_token %}` in all POST templates
4. Write form validation tests (80% coverage required)

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

1. **Build `allergies/constants/compounds.py`** ← *active now, Gate 4 prereq*
   - Migrate every entry from `choices.py` to `CompoundEntry` NamedTuple rows
   - Apply transformation rules: INCI extraction, CAS lookup, group
     decomposition (parabens, formaldehyde releasers, PEG compounds)
   - Set `eu_annex_iii` and `regulatory_ref` on all fragrance and
     preservative entries
   - No stubs — every entry from `choices.py` must appear; output is
     `ALL_COMPOUNDS: Final[tuple[CompoundEntry, ...]]`
   - Do not import from `choices.py` in the new file
   - Do not write the seed migration yet — that is step 0b, after this file
     is complete and reviewed

2. **Write seed migration (Gate 4 prereq step 0b)** — after item 1 is done
   - `allergies/migrations/XXXX_seed_allergen_catalog`
   - Reads from `ALL_COMPOUNDS`, populates `Allergen` table
   - Adds `label` field to `Allergen`; `__str__` switches to `self.label`
   - After this lands: delete `FLAT_ALLERGEN_LABEL_MAP` import from `models.py`

---

*Do not start Gate 4 task 1 (forms.py) until items 1 and 2 above are done.*
---

## Known Gaps (Exist but Incomplete)

| Item | What Exists | What's Missing |
|------|-------------|----------------|
| `allergies/constants/choices.py` | Architecture correct; map/lookup
functions solid | `compounds.py` migration in progress —
`ALL_COMPOUNDS` tuple being built. Seed migration (Gate 4 prereq)
not yet written. `choices.py` role shrinks after seed migration lands. |
| `allergies/models.py` | `Allergen` and `UserAllergy` models; JSONField key validation in `clean()` | Unverified against actual file on disk — confirm matches uploaded version |
| `allergies/views.py` | Error handling implemented; GET logging implemented | CREATE/UPDATE/DELETE logging and POST logic blocked until Gate 4 |
| `skincare_project/views.py` | Logging complete; `home` and `product` GET views exist | `product` POST handler not implemented (Gate 4) |
| `allergies/tests/test_models.py` | Some `Allergen` tests exist | `UserAllergy` tests missing — confirmed TODO at L59 |
| `users/tests.py` | 382 lines exist | Scope of coverage unknown — audit required |
| `allergies/constants/choices.py` display maps | `FLAT_ALLERGEN_LABEL_MAP`, `CATEGORY_TO_ALLERGENS_MAP`, and `FORM_ALLERGIES_CHOICES` are built from static tuples at import time | Any allergen added via the admin panel won't appear in these maps — silent divergence between DB and display layer. Acceptable while admin is seed-only. Post-Gate 4, allergen labels and category groupings must be read from the database, not this file. Treat this file's role as shrinking after the seed migration lands. |
| `ChoiceItem` type alias in `choices.py` | Defined as `tuple[str, str]` | Mypy won't catch a malformed entry like `("glycolic_acid",)` — tuple covariance + `...` weakens the check. Runtime crash is the first signal. Fix at Gate 4 when form rendering makes this a live risk: replace `ChoiceItem` with a `TypedDict` or `NamedTuple` with named fields `value` and `label`, which mypy checks strictly. |

---

## Blocked Features

These cannot be started until the gates above are done:

- 🚫 **Product safety check POST handler** (`skincare_project/views.py`) — needs Gate 4 forms/validation first
- 🚫 **User-facing allergy forms** — needs Gate 4 (forms)

---

## Planned (Post-Gates, Not Started)

- **Synonym Mapper / `AllergenAlias` model** — many-to-one table mapping all known surface forms of an ingredient (INCI name, common name, abbreviation) to a canonical `allergen_key`. No model, migration, service layer, or design document exists yet. Required before the product safety check can be considered production-accurate.

- **`choices.py` file split (`categories.py` + `allergens.py`)** — Currently
  blocked by `models.py` importing `FLAT_ALLERGEN_LABEL_MAP` for `__str__`.
  Split becomes clean only after the seed migration adds a `label` field to
  `Allergen` and `__str__` switches to `self.label`, dropping the map import.
  Do not split before that migration exists.

- **Seed migration** — now sequenced as Gate 4 prereq step 0b above.
Depends on `compounds.py` completion.

- **`FORM_ALLERGIES_CHOICES` 3-tuple structure** — Correct for Gate 4. The
  `(category_key, optgroup_label, choices_list)` structure maps to Django
  `<optgroup>` rendering and correctly supports multiple optgroups per database
  category (e.g. "Acids & Exfoliants" and "Botanicals" both under `contact`).
  Do not change this structure at Gate 4.

  Will need replacement — not refactoring — if the allergen catalog grows beyond
  ~100 entries and a flat `<select>` becomes poor UX. At that point, switch to
  an autocomplete widget (e.g. Select2) backed by a JSON endpoint querying the
  `Allergen` table directly. When that happens, `FORM_ALLERGIES_CHOICES` becomes
  irrelevant and can be deleted. That is a UX decision, not an architecture one.

  Synonyms (`AllergenAlias`) never belong in this structure — they live in the
  matching pipeline, which is a separate code path from the form.

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
*Last updated: 3/25/2026 12:12 AM — STATUS sync: Gate 3 heading corrected, Gate 4/5 blockers updated, Known Gaps stale rows cleaned up.*
