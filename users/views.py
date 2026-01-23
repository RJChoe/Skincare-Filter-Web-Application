import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Module-level logger setup
logger = logging.getLogger(__name__)


# Create your views here.
def user_list(request: HttpRequest) -> HttpResponse:
    # minimal-view: no-logger-needed
    return render(request, "user/user_list.html")
