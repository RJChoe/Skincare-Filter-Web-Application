import logging

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import CustomUser

# Module-level logger setup
logger = logging.getLogger(__name__)


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    # minimal-view: no-logger-needed
    # Profile fields are available via the built-in {{ user }} context processor
    return render(request, "user.html")


@user_passes_test(lambda u: u.is_staff)
def user_list(request: HttpRequest) -> HttpResponse:
    # minimal-view: no-logger-needed
    users = CustomUser.objects.all()
    return render(request, "user/user_list.html", {"users": users})
