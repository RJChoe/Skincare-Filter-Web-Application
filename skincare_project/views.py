import logging

from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

# Module-level logger setup
logger = logging.getLogger(__name__)

# When implementing forms/POST handlers, import these:
# from django.db import transaction
# from allergies.exceptions import InvalidIngredientError
# from allergies.models import UserAllergy


def home(request: HttpRequest) -> HttpResponse:
    # minimal-view: no-logger-needed
    return render(request, "home.html")


@require_http_methods(["GET", "POST"])
def product(request: HttpRequest) -> HttpResponse:
    """Product ingredient checker with error handling.

    GET: Display product input form
    POST: Check ingredients against user allergies (future implementation)
    """

    if request.method == "GET":
        # minimal-view: no-logger-needed
        return render(request, "product.html")

    # POST request - check ingredients (FUTURE IMPLEMENTATION after Gate 4)
    try:
        logger.info(
            f"User {request.user.id if request.user.is_authenticated else 'anonymous'} checking product ingredients"
        )

        # Validate user is authenticated
        if not request.user.is_authenticated:
            logger.warning("Unauthenticated user attempted product check")
            return JsonResponse(
                {"error": "Authentication required"},
                status=401,
            )

        # TODO: Implement ingredient parsing and allergen checking
        # This will be completed in Gate 4 (Forms & Validation)
        logger.warning("POST handler not yet fully implemented")
        return JsonResponse(
            {"error": "Feature coming soon"},
            status=501,  # Not Implemented
        )

        # FUTURE: Ingredient checking logic will go here
        # ingredients = request.POST.get("ingredients", "").strip()
        # if not ingredients:
        #     raise InvalidIngredientError("Ingredient list cannot be empty")
        #
        # ingredient_list = [i.strip().lower() for i in ingredients.split(",")]
        #
        # user_allergies = UserAllergy.objects.select_related('allergen').filter(
        #     user=request.user,
        #     is_active=True
        # )
        #
        # matches = []
        # for allergy in user_allergies:
        #     allergen_label = allergy.allergen.allergen_label.lower()
        #     if any(allergen_label in ingredient for ingredient in ingredient_list):
        #         matches.append({
        #             'allergen': allergy.allergen.allergen_label,
        #             'severity': allergy.severity_level,
        #             'category': allergy.allergen.get_category_display(),
        #         })
        #         logger.info(
        #             f"Match found: User {request.user.id} allergen '{allergen_label}' "
        #             f"in ingredients (severity: {allergy.severity_level})"
        #         )
        #
        # return JsonResponse({
        #     'success': True,
        #     'matches': matches,
        #     'total_checked': len(ingredient_list)
        # })

    except Exception as e:
        logger.error(
            f"Unexpected error in product check for user {request.user.id if request.user.is_authenticated else 'anonymous'}: {e}",
            exc_info=True,
        )
        return JsonResponse(
            {"error": "An unexpected error occurred. Please try again later."},
            status=500,
        )
