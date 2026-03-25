# Project Status — Skincare Allergy Filter

> **This is the only file that changes after each work session.**
> Update it when a task is finished, a gap is discovered, or a gate is completed.
> Do not embed status in `copilot-instructions.md` — keep that file stable.

---

## Gate Summary

| Gate | Name | Status |
|------|------|--------|
| 1 | Dependencies | ✅ Complete |
| 2 | Logging Infrastructure | 🚧 In Progress |
| 3 | Error Handling | 🚧 In Progress |
| 4 | Forms & Validation | ❌ Blocked (Gates 2–3 incomplete) |
| 5 | Tests | ❌ Blocked (Gates 2–3 incomplete) |

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
| `allergies/views.py` | ❌ Incomplete | present — GET access logged. CREATE/UPDATE/DELETE logging blocked until POST handler (Gate 4) |
| `skincare_project/views.py` | ✅ Complete | present — product POST handler partially stubbed with correct logging |
| `skincare_project/settings.py` LOGGING config | ✅ Complete | Existence confirmed from source |

### Gate 3: Error Handling — 🚧 In Progress

**Complete when:** all view functions have `try/except` with user-friendly error
rendering, `@transaction.atomic` on all writes, and `allergies/exceptions.py`
exists with domain exception classes.

| Item | Status | Notes |
|------|--------|-------|
| `try/except` in `allergies/views.py` | ❌ Incomplete | Not implemented |
| `try/except` in `skincare_project/views.py` | ❌ Incomplete | Not implemented |
| `@transaction.atomic` on multi-model writes | ❌ Unverified | Not confirmed from source |
| `allergies/exceptions.py` | ❌ Unverified | File existence not confirmed |
| `AllergenNotFoundError` class | ❌ Unverified | Depends on above |
| `InvalidIngredientError` class | ❌ Unverified | Depends on above |
| Validation errors surfaced (no 500s) | ❌ Unverified | Not confirmed from source |

### Gate 4: Forms & Validation — ❌ Blocked

**Blocked by:** Gates 2 and 3 not complete.

Tasks (do not start until Gates 2–3 are done):
1. Create `allergies/forms.py` with `UserAllergyForm`
2. Implement dynamic `allergen_key` filtering (category → allergen cascading)
3. Add `{% csrf_token %}` in all POST templates
4. Write form validation tests (80% coverage required)

### Gate 5: Tests — ❌ Blocked

**Blocked by:** Gates 2 and 3 not complete. Run in parallel with Gate 4 once unblocked.

Tasks:
1. Complete `allergies/tests/test_models.py` — TODO at L59 covers `UserAllergy`
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

1. **Verify `allergies/admin.py`** — open the file, confirm `logger = logging.getLogger(__name__)` is present at module level and used in admin actions
2. **Add logging to `allergies/views.py`** — module-level logger; INFO on allergy create/update/delete; ERROR with `exc_info=True` on exceptions
3. **Add logging to `skincare_project/views.py`** — same pattern; required before product safety POST handler can be implemented
4. **Verify/create `allergies/exceptions.py`** — must contain `AllergenNotFoundError` and `InvalidIngredientError`
5. **Add `try/except` + `@transaction.atomic` to all views** — follow pattern in `copilot-instructions.md` → Error Handling & Resilience section
6. **Complete `choices.py`** — remove all `# ... and so on` stubs; fill in full EU Annex III 2023-grounded ingredient lists per allergen group (prerequisite for allergen catalog seeding migration)

---

## Known Gaps (Exist but Incomplete)

| Item | What Exists | What's Missing |
|------|-------------|----------------|
| `allergies/constants/choices.py` | Architecture correct; map/lookup functions solid | Allergen lists have placeholder stubs — not production-ready |
| `allergies/models.py` | `Allergen` and `UserAllergy` models; JSONField key validation in `clean()` | Unverified against actual file on disk — confirm matches uploaded version |
| `allergies/views.py` | File exists | Logging, error handling, and any POST logic not implemented |
| `skincare_project/views.py` | `home` and `product` GET views exist | No logging; `product` POST handler not implemented |
| `allergies/tests/test_models.py` | Some `Allergen` tests exist | `UserAllergy` tests missing — confirmed TODO at L59 |
| `users/tests.py` | 382 lines exist | Scope of coverage unknown — audit required |
| `allergies/exceptions.py` | May or may not exist | Contents unverified |
| `allergies/constants/choices.py` display maps | `FLAT_ALLERGEN_LABEL_MAP`, `CATEGORY_TO_ALLERGENS_MAP`, and `FORM_ALLERGIES_CHOICES` are built from static tuples at import time | Any allergen added via the admin panel won't appear in these maps — silent divergence between DB and display layer. Acceptable while admin is seed-only. Post-Gate 4, allergen labels and category groupings must be read from the database, not this file. Treat this file's role as shrinking after the seed migration lands. |
| `ChoiceItem` type alias in `choices.py` | Defined as `tuple[str, str]` | Mypy won't catch a malformed entry like `("glycolic_acid",)` — tuple covariance + `...` weakens the check. Runtime crash is the first signal. Fix at Gate 4 when form rendering makes this a live risk: replace `ChoiceItem` with a `TypedDict` or `NamedTuple` with named fields `value` and `label`, which mypy checks strictly. |

---

## Blocked Features

These cannot be started until the gates above are done:

- 🚫 **Product safety check POST handler** (`skincare_project/views.py`) — needs logging + error handling in that file first
- 🚫 **User-facing allergy forms** — needs Gate 4 (forms) which needs Gates 2–3
- 🚫 **Users app URL routing** — `path('users/', include('users.urls'))` — needs views to have logging and error handling first

---

## Planned (Post-Gates, Not Started)

- **Synonym Mapper / `AllergenAlias` model** — many-to-one table mapping all known surface forms of an ingredient (INCI name, common name, abbreviation) to a canonical `allergen_key`. No model, migration, service layer, or design document exists yet. Required before the product safety check can be considered production-accurate.

- **`choices.py` file split (`categories.py` + `allergens.py`)** — Currently
  blocked by `models.py` importing `FLAT_ALLERGEN_LABEL_MAP` for `__str__`.
  Split becomes clean only after the seed migration adds a `label` field to
  `Allergen` and `__str__` switches to `self.label`, dropping the map import.
  Do not split before that migration exists.

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
*Last updated: 3/24/2026 6:11 PM manually — update this line after each work session.*
