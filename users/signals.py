"""Signal handlers for automatic allergy timestamp updates."""

import logging

from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

# Module-level logger setup
logger = logging.getLogger(__name__)


def update_user_allergy_timestamp(user_ids: set[int]) -> None:
    """
    Bulk update allergies_updated_at timestamp for multiple users.

    This function is called after UserAllergy changes are committed to batch
    timestamp updates for improved performance.

    Args:
        user_ids: Set of user IDs whose allergy profiles have changed.
    """
    if not user_ids:
        return

    # Import here to avoid circular dependency
    from users.models import CustomUser

    try:
        timestamp = timezone.now()
        updated_count = CustomUser.objects.filter(id__in=user_ids).update(
            allergies_updated_at=timestamp
        )
        logger.info(
            f"Batch updated allergies_updated_at for {updated_count} users: {sorted(user_ids)}"
        )
    except Exception as e:
        logger.error(
            f"Failed to batch update allergies_updated_at for users {user_ids}: {e}",
            exc_info=True,
        )


@receiver(post_save, sender="allergies.UserAllergy")
def user_allergy_saved(sender, instance, created, **kwargs) -> None:
    """
    Signal handler triggered when a UserAllergy is created or updated.

    Updates the user's allergies_updated_at timestamp using batched updates
    via transaction.on_commit() to ensure changes are persisted first.

    Args:
        sender: The model class (UserAllergy).
        instance: The saved UserAllergy instance.
        created: Boolean indicating if this is a new record.
        **kwargs: Additional keyword arguments from the signal.
    """
    action = "created" if created else "updated"
    logger.debug(
        f"UserAllergy {action}: user_id={instance.user_id}, allergen={instance.allergen.allergen_key}"
    )

    # Collect user IDs to update (could batch multiple signals in same transaction)
    user_ids = {instance.user_id}

    # Schedule timestamp update after transaction commits
    transaction.on_commit(lambda: update_user_allergy_timestamp(user_ids))


@receiver(post_delete, sender="allergies.UserAllergy")
def user_allergy_deleted(sender, instance, **kwargs) -> None:
    """
    Signal handler triggered when a UserAllergy is deleted.

    Updates the user's allergies_updated_at timestamp using batched updates
    via transaction.on_commit() to ensure deletion is persisted first.

    Args:
        sender: The model class (UserAllergy).
        instance: The deleted UserAllergy instance.
        **kwargs: Additional keyword arguments from the signal.
    """
    logger.debug(
        f"UserAllergy deleted: user_id={instance.user_id}, allergen={instance.allergen.allergen_key}"
    )

    # Collect user IDs to update
    user_ids = {instance.user_id}

    # Schedule timestamp update after transaction commits
    transaction.on_commit(lambda: update_user_allergy_timestamp(user_ids))
