import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

# Module-level logger setup
logger = logging.getLogger(__name__)


# Create your views here.
def allergies_list(request):
    """Display list of user's allergies with error handling."""
    try:
        logger.info(
            f"User {request.user.id if request.user.is_authenticated else 'anonymous'} accessed allergies list"
        )

        # Check authentication
        if not request.user.is_authenticated:
            logger.warning("Unauthenticated user attempted to access allergies list")
            messages.warning(request, "Please log in to view your allergies.")
            # For now, just render empty template. Later: redirect to login

        # Future: Fetch user allergies from database
        # user_allergies = UserAllergy.objects.select_related('allergen').filter(
        #     user=request.user,
        #     is_active=True
        # )

        return render(request, "allergies/allergies_list.html")

    except PermissionDenied:
        logger.warning(f"Permission denied for user {request.user.id}")
        messages.error(request, "You don't have permission to view this page.")
        return render(request, "allergies/allergies_list.html", status=403)

    except Exception as e:
        # Catch unexpected errors
        logger.error(
            f"Unexpected error in allergies_list for user {request.user.id if request.user.is_authenticated else 'anonymous'}: {e}",
            exc_info=True,
        )
        messages.error(request, "An unexpected error occurred. Please try again later.")
        return render(request, "allergies/allergies_list.html", status=500)


# if request.method == 'POST':
# process request: Handle form submission for adding new allergies
