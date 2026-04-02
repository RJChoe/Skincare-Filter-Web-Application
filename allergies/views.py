import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from allergies.forms import AllergenSelectForm, UserAllergyEditForm
from allergies.models import UserAllergy

# Module-level logger setup
logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
@login_required
def allergy_list(request: HttpRequest) -> HttpResponse:
    """Display user's allergen profile and the add-allergen form."""
    assert request.user.is_authenticated
    try:
        logger.info(f"User {request.user.pk} accessed allergen profile")
        user_allergies = (
            UserAllergy.objects.filter(user=request.user, is_active=True)
            .select_related("allergen")
            .order_by("allergen__subcategory", "allergen__label")
        )
        form = AllergenSelectForm()
        grouped_allergens = form.get_grouped_allergens()
        return render(
            request,
            "allergies/allergies_list.html",
            {
                "user_allergies": user_allergies,
                "form": form,
                "grouped_allergens": grouped_allergens,
            },
        )
    except Exception as e:
        logger.error(
            f"Unexpected error in allergy_list for user {request.user.pk}: {e}",
            exc_info=True,
        )
        messages.error(request, "An unexpected error occurred. Please try again later.")
        return render(
            request,
            "allergies/allergies_list.html",
            {
                "user_allergies": [],
                "form": AllergenSelectForm(),
                "grouped_allergens": [],
            },
            status=500,
        )


@require_POST
@login_required
def create_allergies(request: HttpRequest) -> HttpResponse:
    """Create UserAllergy rows for each selected allergen."""
    assert request.user.is_authenticated
    try:
        with transaction.atomic():
            form = AllergenSelectForm(request.POST)
            if not form.is_valid():
                messages.error(request, "Invalid allergen selection.")
                return redirect("allergies:list")

            created_count = 0
            for allergen in form.cleaned_data["allergens"]:
                _, created = UserAllergy.objects.get_or_create(
                    user=request.user,
                    allergen=allergen,
                )
                if created:
                    logger.info(
                        f"User {request.user.pk} added allergen {allergen.allergen_key}"
                    )
                    created_count += 1

            if created_count:
                messages.success(
                    request,
                    f"{created_count} allergen(s) added to your profile.",
                )
            else:
                messages.info(
                    request, "Selected allergens were already in your profile."
                )

            return redirect("allergies:list")

    except ValidationError as e:
        logger.warning(
            f"ValidationError in create_allergies for user {request.user.pk}: {e}"
        )
        messages.error(request, str(e))
        return redirect("allergies:list")
    except Exception as e:
        logger.error(
            f"Unexpected error in create_allergies for user {request.user.pk}: {e}",
            exc_info=True,
        )
        messages.error(request, "An unexpected error occurred. Please try again later.")
        return redirect("allergies:list")


@require_http_methods(["GET", "POST"])
@login_required
def edit_allergy(request: HttpRequest, pk: int) -> HttpResponse:
    """Edit detail fields on a single UserAllergy."""
    assert request.user.is_authenticated
    user_allergy = get_object_or_404(UserAllergy, pk=pk, user=request.user)

    if request.method == "GET":
        try:
            logger.info(
                f"User {request.user.pk} accessed edit form for UserAllergy {pk}"
            )
            form = UserAllergyEditForm(instance=user_allergy)
            return render(
                request,
                "allergies/edit_allergy.html",
                {"form": form, "user_allergy": user_allergy},
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in edit_allergy GET for user {request.user.pk}: {e}",
                exc_info=True,
            )
            messages.error(
                request, "An unexpected error occurred. Please try again later."
            )
            return redirect("allergies:list")

    # POST
    try:
        with transaction.atomic():
            form = UserAllergyEditForm(request.POST, instance=user_allergy)
            if form.is_valid():
                form.save()
                logger.info(
                    f"User {request.user.pk} updated UserAllergy {pk} "
                    f"(allergen: {user_allergy.allergen.allergen_key})"
                )
                messages.success(request, "Allergy details updated.")
                return redirect("allergies:list")
            return render(
                request,
                "allergies/edit_allergy.html",
                {"form": form, "user_allergy": user_allergy},
            )
    except ValidationError as e:
        logger.warning(
            f"ValidationError in edit_allergy POST for user {request.user.pk}: {e}"
        )
        messages.error(request, str(e))
        return render(
            request,
            "allergies/edit_allergy.html",
            {
                "form": UserAllergyEditForm(instance=user_allergy),
                "user_allergy": user_allergy,
            },
        )
    except Exception as e:
        logger.error(
            f"Unexpected error in edit_allergy POST for user {request.user.pk}: {e}",
            exc_info=True,
        )
        messages.error(request, "An unexpected error occurred. Please try again later.")
        return redirect("allergies:list")


@require_POST
@login_required
def delete_allergy(request: HttpRequest, pk: int) -> HttpResponse:
    """Remove a UserAllergy entry."""
    assert request.user.is_authenticated
    user_allergy = get_object_or_404(UserAllergy, pk=pk, user=request.user)
    try:
        with transaction.atomic():
            allergen_key = user_allergy.allergen.allergen_key
            user_allergy.delete()
            logger.info(
                f"User {request.user.pk} deleted UserAllergy {pk} "
                f"(allergen: {allergen_key})"
            )
            messages.success(request, "Allergen removed from your profile.")
            return redirect("allergies:list")
    except Exception as e:
        logger.error(
            f"Unexpected error in delete_allergy for user {request.user.pk}: {e}",
            exc_info=True,
        )
        messages.error(request, "An unexpected error occurred. Please try again later.")
        return redirect("allergies:list")
