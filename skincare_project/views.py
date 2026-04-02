import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from allergies.exceptions import InvalidIngredientError
from allergies.services import check_ingredients
from users.models import CustomUser

# Module-level logger setup
logger = logging.getLogger(__name__)


def home(request: HttpRequest) -> HttpResponse:
    # minimal-view: no-logger-needed
    return render(request, "home.html")


@login_required
@require_http_methods(["GET", "POST"])
def product(request: HttpRequest) -> HttpResponse:
    """Product ingredient checker.

    GET: Display product input form
    POST: Check ingredients against user allergies
    """

    if request.method == "GET":
        logger.info(f"User {request.user.id} accessed product page")
        return render(request, "product.html")

    # POST — check ingredients
    assert isinstance(request.user, CustomUser)
    ingredient_text = request.POST.get("ingredients", "")
    try:
        matches = check_ingredients(ingredient_text, request.user)
        logger.info(
            f"User {request.user.id} product check complete: {len(matches)} match(es)"
        )
        return render(
            request,
            "product.html",
            {
                "checked": True,
                "matches": matches,
                "ingredients": ingredient_text,
            },
        )
    except InvalidIngredientError as e:
        logger.warning(f"InvalidIngredientError for user {request.user.id}: {e}")
        return render(
            request,
            "product.html",
            {
                "error": str(e),
                "ingredients": ingredient_text,
            },
        )
    except Exception as e:
        logger.error(
            f"Unexpected error in product check for user {request.user.id}: {e}",
            exc_info=True,
        )
        return render(
            request,
            "product.html",
            {
                "error": "An unexpected error occurred. Please try again later.",
                "ingredients": ingredient_text,
            },
            status=500,
        )
