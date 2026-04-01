# Skincare Project Structure

├── 📁 ROOT CONFIGURATION
│   ├── ARCHITECTURE.md          # System design & data flow
│   ├── PRODUCT.md               # Requirements & Scope
│   ├── STATUS.md                # Roadmap & Current progress
│   ├── pyproject.toml           # uv dependencies (PEP 621)
│   ├── manage.py                # Django entry point
│   ├── .env.example             # Required environment variables
│   ├── .python-version          # Pins Python 3.13
│   ├── conftest.py              # Shared pytest fixtures (Canonical Source)
│   └── .pre-commit-config.yaml  # Hooks (incl. migration naming enforcement)
│
├── 📁 DOCUMENTATION (docs/dev/)
│   ├── ADMIN.md, DEPLOYMENT.md, FORMS.md
│   ├── LOGGING.md, MIGRATIONS.md, SECURITY.md
│   └── TESTING.md
│
├── 📁 CORE: skincare_project/
│   ├── settings.py              # Main Django config
│   ├── urls.py                  # Root URL dispatcher
│   └── wsgi.py / asgi.py        # Server interfaces
│
├── 📁 APP: ALLERGIES/           [Ingredient & Filter Logic]
│   ├── migrations/              # DB Migration history
│   ├── models.py                # DB Schema (Allergen + UserAllergy)
│   ├── admin.py                 # Admin panel configuration
│   ├── views.py                 # Filtering logic
│   ├── urls.py                  # App-level routing
│   ├── constants/compounds.py     # Static mapping data
│   ├── exceptions.py            # Exceptions
│   ├── templates/allergies/     # List views & partials
│   └── tests/
│       ├── test_models.py       # [!] Incomplete (Ref: L59)
│       ├── test_views.py        # [!] NOT YET VERIFIED
│       ├── test_exceptions.py   # [!] NOT YET VERIFIED
│       └── test_admin_error_handling.py
│
├── 📁 APP: USERS/               [Auth & Profile Management]
│   ├── migrations/              # DB Migration history
│   ├── models.py                # Custom User Model
│   ├── admin.py                 # CustomUser admin config
│   ├── managers.py              # User creation logic
│   ├── signals.py               # Post-save triggers
│   ├── validators.py            # Custom input validation
│   ├── views.py                 # Profile/User logic
│   ├── urls.py                  # [!] Not yet included in Root URLs
│   ├── tests.py                 # 382 lines (Coverage unaudited)
│   └── _log_utils.py            # Logging helpers (Gate 2 scope)
│
├── 📁 GLOBAL UI (templates/)
│   ├── base.html                # Main skeleton
│   ├── layout.html              # Structural wrapper
│   ├── home.html                # Landing page
│   └── product.html             # Product detail view
│
└── 📁 STATIC & ASSETS/
│    ├── css/main.css             # Global styles
│    └── assets/                  # Workflow diagrams & images
│
└── 📁 .github
│   ├── pull_request_template.md  # Pull Request template
│   │
│   ├── workflows/
│   │   ├── ci.yml                # copilot-instrcutions
│   │   └── uv-export.yml         # uv-export file
│   │
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md         # bug report instructions
│   │   └── feature_request.md    # feature request
│   │
│   ├── scripts/
│   │   └── annotate_safety.py     # annotate safety
│   │
│   └── instructions/
│       └── copilot-instructions.md # copilot-instrcutions.md
