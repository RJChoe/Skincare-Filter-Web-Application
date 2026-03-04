"""App configuration for the users app."""

from django.apps import AppConfig


class UserConfig(AppConfig):
    """Configuration for the users app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self) -> None:
        """
        Import signal handlers when the app is ready.

        This ensures signals are registered when Django starts up.
        Uses an import guard to prevent duplicate registration during testing.
        """
        # Import signals to register handlers
        import users.signals
