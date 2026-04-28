# Skincare Project Structure

## Legend
- `[!]` — incomplete or unverified; do not rely on without reading the file
- No marker — present on disk; purpose is noted where clear

---

```
📁 ROOT
├── manage.py                        # Django entry point
├── conftest.py                      # Shared pytest fixtures (canonical source)
├── pyproject.toml                   # uv dependencies (PEP 621)
├── .python-version                  # Pins Python 3.13
├── .env                             # Local secrets (gitignored)
├── .env.example                     # Required env var reference
├── .gitignore
├── .gitattributes
├── .gitleaks.toml                   # Secret scanning config
├── .safety-project.ini
├── .pre-commit-config.yaml          # Hooks (incl. migration naming enforcement)
├── codecov.yml
├── LICENSE
├── README.md
├── ARCHITECTURE.md                  # System design & data flow
├── PRODUCT.md                       # Requirements & scope
├── STATUS.md                        # Roadmap & current progress
├── PROJECT_TREE.md                  # This file
│
├── 📁 .claude/
│   └── settings.local.json          # Claude Code project permissions
│
├── 📁 .vscode/
│   └── settings.json
│
├── 📁 .github/
│   ├── pull_request_template.md
│   ├── actions/
│   │   └── setup-python-uv/
│   │       └── action.yml           # Reusable uv setup action
│   ├── workflows/
│   │   ├── ci.yml                   # Main CI pipeline
│   │   └── uv-export.yml            # Dependency export workflow
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── scripts/
│   │   └── annotate_safety.py       # Safety annotation helper
│   └── instructions/
│       └── copilot-instructions.md
│
├── 📁 docs/dev/
│   ├── adr/
│   │   └── 0001-constants-compounds-decision.md
│   ├── ADMIN.md
│   ├── DEPLOYMENT.md
│   ├── FORMS.md
│   ├── LOGGING.md
│   ├── MIGRATIONS.md
│   ├── SECURITY.md
│   └── TESTING.md
│
├── 📁 skincare_project/              [Django project package]
│   ├── __init__.py
│   ├── settings.py                  # Main Django config
│   ├── urls.py                      # Root URL dispatcher
│   ├── views.py                     # Project-level views (e.g. 404/500)
│   ├── wsgi.py
│   ├── asgi.py
│   └── tests/
│       ├── __init__.py
│       └── test_views_error_handling.py
│
├── 📁 allergies/                     [Ingredient & filter logic app]
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                    # Allergen + UserAllergy schema
│   ├── admin.py                     # Admin panel config
│   ├── views.py                     # Filtering logic & check endpoint
│   ├── urls.py                      # App-level routing
│   ├── forms.py
│   ├── services.py
│   ├── exceptions.py
│   ├── constants/
│   │   └── compounds.py             # Static allergen→compound mapping
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── templates/allergies/         # App-local templates (may duplicate global)
│   │   ├── allergies_list.html
│   │   └── edit_allergy.html
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py           # [!] Previously flagged incomplete
│       ├── test_views.py
│       ├── test_views_error_handling.py
│       ├── test_forms.py
│       ├── test_services.py
│       ├── test_exceptions.py
│       ├── test_constants.py
│       └── test_admin_error_handling.py
│
├── 📁 users/                         [Auth & profile management app]
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                    # Custom User model
│   ├── admin.py                     # CustomUser admin config
│   ├── managers.py                  # User creation logic
│   ├── signals.py                   # Post-save triggers
│   ├── validators.py                # Custom input validation
│   ├── views.py
│   ├── urls.py                      # [!] Not confirmed included in root URLs
│   ├── _log_utils.py                # Logging helpers
│   ├── tests.py                     # [!] Coverage unaudited
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   └── templates/users/
│       ├── user.html
│       └── user_list.html
│
├── 📁 templates/                     [Global template overrides]
│   ├── base.html                    # Main skeleton
│   ├── layout.html                  # Structural wrapper
│   ├── home.html                    # Landing page
│   ├── product.html                 # Product detail/check view
│   └── allergies/
│       ├── allergies_list.html
│       └── edit_allergy.html
│
├── 📁 static/
│   ├── favicon.svg
│   ├── css/
│   │   └── main.css
│   └── js/
│       └── main.js
│
├── 📁 assets/
│   └── workflow_allergy_filter.png  # Workflow diagram
│
├── 📁 htmlcov/                       [Generated HTML coverage report — gitignored]
│   └── index.html  (+ supporting files)
│
└── 📁 _private_notes/                [Local design notes — not committed]
    └── choices_py_redesign_proposal_2.md
```

---

### Tool/cache directories (contents excluded from tree)

| Directory        | Purpose                        |
|------------------|-------------------------------|
| `.venv/`         | uv-managed virtual environment |
| `.mypy_cache/`   | mypy type-check cache          |
| `.pytest_cache/` | pytest run cache               |
| `.ruff_cache/`   | ruff lint cache                |
