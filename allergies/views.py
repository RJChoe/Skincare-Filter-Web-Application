import logging

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from allergies.constants.choices import FORM_ALLERGIES_CHOICES

# Module-level logger setup
logger = logging.getLogger(__name__)


# Create your views here.
def allergies_list(request: HttpRequest) -> HttpResponse:
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

        return render(
            request,
            "allergies/allergies_list.html",
            {"FORM_ALLERGIES_CHOICES": FORM_ALLERGIES_CHOICES},
        )

    except Exception as e:
        # Catch unexpected errors
        logger.error(
            f"Unexpected error in allergies_list for user {request.user.id if request.user.is_authenticated else 'anonymous'}: {e}",
            exc_info=True,
        )
        messages.error(request, "An unexpected error occurred. Please try again later.")
        return render(
            request,
            "allergies/allergies_list.html",
            {"FORM_ALLERGIES_CHOICES": FORM_ALLERGIES_CHOICES},
            status=500,
        )


# if request.method == 'POST':
# process request: Handle form submission for adding new allergies
