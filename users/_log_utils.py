"""GDPR-safe logging utilities for the users app.

Provides HMAC-based correlation tokens so log entries can be traced
across a request without exposing raw PII (email addresses).

Note: Rotating SECRET_KEY intentionally invalidates old tokens —
this is desirable from a privacy standpoint.
"""

import hashlib
import hmac

from django.conf import settings


def email_token(email: str) -> str:
    """
    Return a 12-character HMAC-SHA256 hex token derived from the given email.

    The token is keyed by SECRET_KEY, making it non-reversible without access
    to the secret. Safe to write to logs, monitoring dashboards, and error
    trackers. Consistent within a single SECRET_KEY lifetime, allowing
    log correlation across entries for the same address.

    Args:
        email: The raw email address to tokenise.

    Returns:
        str: A 12-character lowercase hex string.
    """
    if not email:
        return "000000000000"  # Sentinel — distinguishable, non-colliding
    return hmac.new(
        settings.SECRET_KEY.encode(),
        email.encode(),
        hashlib.sha256,
    ).hexdigest()[:12]
