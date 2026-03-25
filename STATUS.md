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
| `allergies/exceptions.py` | ✅ Complete | File exists |
| `AllergenNotFoundError` class | ✅ Complete | Class exists |
| `InvalidIngredientError` class | ✅ Complete | Class exists |
| Validation errors surfaced (no 500s) | ❌ Unverified | Not confirmed from source |

### Gate 4: Forms & Validation — ❌ Blocked

**Blocked by:** Gates 2 and 3 not complete.

Tasks (do not start until Gates 2–3 are done):
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

1. **Complete Gates 2–3 remaining items (in parallel)**
   - `allergies/views.py` — add `try/except` + `@transaction.atomic`;
     CREATE/UPDATE/DELETE logging deferred until POST handler (Gate 4)
   - `skincare_project/views.py` — add `try/except` + `@transaction.atomic`
   - Verify validation errors surface correctly (no 500s)
   - Confirm `@transaction.atomic` on all multi-model writes

2. **Build `allergies/constants/compounds.py`** ← *active now, Gate 4 prereq*
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

3. **Write seed migration (Gate 4 prereq step 0b)** — after item 2 is done
   - `allergies/migrations/XXXX_seed_allergen_catalog`
   - Reads from `ALL_COMPOUNDS`, populates `Allergen` table
   - Adds `label` field to `Allergen`; `__str__` switches to `self.label`
   - After this lands: delete `FLAT_ALLERGEN_LABEL_MAP` import from `models.py`

---

*Do not start Gate 4 task 1 (forms.py) until items 1, 2, and 3 above are done.*
---

## Known Gaps (Exist but Incomplete)

| Item | What Exists | What's Missing |
|------|-------------|----------------|
| `allergies/constants/choices.py` | Architecture correct; map/lookup
functions solid | `compounds.py` migration in progress —
`ALL_COMPOUNDS` tuple being built. Seed migration (Gate 4 prereq)
not yet written. `choices.py` role shrinks after seed migration lands. |
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
*Last updated: 3/24/2026 11:12 PM manually — update this line after each work session.*
