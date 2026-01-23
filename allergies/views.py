import logging

from django.shortcuts import render

# Module-level logger setup
logger = logging.getLogger(__name__)


# Create your views here.
def allergies_list(request):
    logger.info(
        f"User {request.user.id if request.user.is_authenticated else 'anonymous'} accessed allergies list"
    )
    return render(request, "allergies/allergies_list.html")


# if request.method == 'POST':
# process request: Handle form submission for adding new allergies
