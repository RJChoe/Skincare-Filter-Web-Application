import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from allergies.constants.choices import FORM_ALLERGIES_CHOICES
from allergies.exceptions import AllergenNotFoundError, InvalidIngredientError

# Module-level logger setup
logger = logging.getLogger(__name__)


# Create your views here.
@require_http_methods(["GET", "POST"])
@login_required
def allergies_list(request: HttpRequest) -> HttpResponse:
    """Display list of user's allergies with error handling."""
    if request.method == "GET":
        try:
            logger.info(f"User {request.user.pk} accessed allergies list")

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
            logger.error(
                f"Unexpected error in allergies_list for user {getattr(request.user, 'pk', 'anonymous')}: {e}",
                exc_info=True,
            )
            messages.error(
                request, "An unexpected error occurred. Please try again later."
            )
            return render(
                request,
                "allergies/allergies_list.html",
                {"FORM_ALLERGIES_CHOICES": FORM_ALLERGIES_CHOICES},
                status=500,
            )

    # POST: Handle form submission for adding new allergies
    try:
        with transaction.atomic():
            logger.info(f"User {request.user.pk} submitted allergies POST")
            # TODO Gate 4: parse form, create/update UserAllergy records
            # CUD logging goes here
            messages.info(request, "Feature coming soon.")
            return render(
                request,
                "allergies/allergies_list.html",
                {"FORM_ALLERGIES_CHOICES": FORM_ALLERGIES_CHOICES},
            )
    except AllergenNotFoundError as e:
        logger.warning(f"AllergenNotFoundError for user {request.user.pk}: {e}")
        messages.error(request, str(e))
    except InvalidIngredientError as e:
        logger.warning(f"InvalidIngredientError for user {request.user.pk}: {e}")
        messages.error(request, str(e))
    except Exception as e:
        logger.error(
            f"Unexpected error in allergies POST for user {request.user.pk}: {e}",
            exc_info=True,
        )
        messages.error(request, "An unexpected error occurred. Please try again later.")
    return render(
        request,
        "allergies/allergies_list.html",
        {"FORM_ALLERGIES_CHOICES": FORM_ALLERGIES_CHOICES},
        status=400,
    )
