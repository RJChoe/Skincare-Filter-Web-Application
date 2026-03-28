## What does this PR do?
<!-- One sentence. What problem does it solve or what feature does it add? -->

## Gate / Work Item
<!-- Which gate or pre-gate task from STATUS.md does this address? -->
- Gate:
- Task:

## Changes
<!-- List the files changed and briefly why -->
- `file.py` —

## Migrations
<!-- If this includes migrations, list them and describe what they do -->
- [ ] No migrations
- [ ] Schema migration: `XXXX_<name>.py` — adds/removes/alters...
- [ ] Data/seed migration: `XXXX_<name>.py` — seeds...

## Pre-merge checklist
- [ ] `uv run pytest --cov --cov-report=term-missing` passes
- [ ] `uv run ruff check . --fix && uv run ruff format .` clean
- [ ] `uv run mypy .` clean
- [ ] No `async def` views, no `pip install`, no 3.14-only features
- [ ] No personal data in logs (user IDs only)
- [ ] STATUS.md updated if a gate or task was completed

## Notes / caveats
<!-- Anything a reviewer should know: known gaps, deferred items, etc. -->
