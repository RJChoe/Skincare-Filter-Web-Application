## What changed
<!-- Lead with gate/task ID where applicable: "Completes Pre-Gate 4 task 0c"
     One sentence on what changed, one on why it was needed.
     Do not repeat the commit message verbatim — expand on it. -->

## Gate / Work Item
<!-- Gate number and task ID from STATUS.md. Examples:
     Gate: Pre-Gate 4 / Task: 0c
     Gate: 4 / Task: 2 (create allergen profile views)
     Gate: 5 / Task: 1 (complete test_models.py) -->
- Gate:
- Task:

## Files changed
<!-- One bullet per file, path relative to project root.
     One line on what the file does in this PR — not what it does in general.
     Order: models → migrations → fixtures → tests → docs
     If more than ~5 files are listed, flag it — minimal blast radius is this project's convention. -->
- `file.py` —

## How to test
<!-- Numbered steps a reviewer can follow to verify the change works. -->
1. `uv run python manage.py migrate`
2. `uv run pytest --cov --cov-report=term-missing`
3. `uv run ruff check .`

## Migrations
<!-- Only include this section when migrations are part of the PR.
     List each file separately and distinguish type explicitly.
     Schema migration — field additions, index/constraint changes
     Data migration — RunPython seeding, backfills
     Note DB resets explicitly: "DB reset — no prior seeded data; fresh initial migration"
     Delete this section entirely if no migrations are included. -->
- [ ] No migrations
- `allergies/migrations/XXXX_name.py` —

## Pre-merge checklist
- [ ] `uv run pytest --cov --cov-report=term-missing` passes
- [ ] `uv run ruff check . --fix && uv run ruff format .` clean
- [ ] `uv run mypy .` clean
- [ ] STATUS.md updated

<!-- Add these when migrations are included: -->
- [ ] `uv run python manage.py migrate` runs without errors
- [ ] Reverse migration tested: `uv run python manage.py migrate allergies <prev>`

<!-- Add this when views, forms, or templates are touched: -->
- [ ] Manual smoke test: [describe the flow]

<!-- Remove inapplicable checklist items before opening the PR. -->

## Design decisions
<!-- Only include when a non-obvious choice was made:
     - A field uses an unusual combination (e.g. blank=False, default="")
     - A catalog entry was intentionally excluded
     - A migration strategy was non-standard (e.g. DB reset instead of additive)
     Reference STATUS.md by section name if the decision is already recorded there.
     Delete this section entirely for straightforward PRs. -->
