# Logging Standards

> Gate 2 reference. See [STATUS.md](../../STATUS.md) for current completion state.

## Setup

Add at module level in **every** view file, admin file, and any model with business logic:

```python
import logging
logger = logging.getLogger(__name__)
```

## Required Files (Gate 2 checklist)

| File | Required | Notes |
|------|----------|-------|
| `allergies/admin.py` | ✅ | Believed present — verify from source |
| `allergies/views.py` | ❌ | Not yet added |
| `skincare_project/views.py` | ❌ | Not yet added |
| Any new view or admin file | ✅ | Required before first commit |

## Log Levels

**INFO — security events:** user-initiated CREATE / UPDATE / DELETE operations.
```python
logger.info(f"User {request.user.id} created allergy {user_allergy.id} "
            f"for allergen {allergen.allergen_key}")
logger.info(f"Admin {request.user.id} deactivated {queryset.count()} allergens")
```

**WARNING — recoverable validation failures:**
```python
logger.warning(f"Validation failed for user {request.user.id}: {e}")
```

**ERROR — unexpected failures:** always include `exc_info=True` for the traceback.
```python
logger.error(f"Unexpected error creating allergy: {e}", exc_info=True)
```

**DEBUG — performance (development only):**
```python
logger.debug(f"Query took {elapsed}s")
```

## GDPR Rule

**Never log personal data.** Log user IDs only — not emails, usernames, or passwords.

```python
# ✅ Correct
logger.info(f"User {request.user.id} updated their profile")

# ❌ Violation
logger.info(f"User {request.user.email} updated their profile")
```

## Configuration

Logging handlers are configured in `skincare_project/settings.py` under the `LOGGING` key.
Production should route to an external service (e.g. Sentry, CloudWatch).
Verify this config exists before marking Gate 2 complete.

## Gate 2 Complete When

Every view function and admin action file has:
- Module-level `logger = logging.getLogger(__name__)`
- INFO log on every CREATE / UPDATE / DELETE
- ERROR log with `exc_info=True` on every exception handler
- No personal data in any log statement
