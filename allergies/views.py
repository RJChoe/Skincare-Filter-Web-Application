import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from allergies.constants.choices import FORM_ALLERGIES_CHOICES

# Module-level logger setup
logger = logging.getLogger(__name__)


# Create your views here.
@login_required
def allergies_list(request: HttpRequest) -> HttpResponse:
    """Display list of user's allergies with error handling."""
    try:
        logger.info(
            f"User {getattr(request.user, 'pk', 'unknown')} accessed allergies list"
        )

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
            f"Unexpected error in allergies_list for user {getattr(request.user, 'pk', 'anonymous')}: {e}",
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
