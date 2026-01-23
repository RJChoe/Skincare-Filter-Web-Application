import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Module-level logger setup
logger = logging.getLogger(__name__)

# functions for rendering pages -processing requests and returning responses
# database, cache, HTML templates, etc. can be integrated here


def home(request: HttpRequest) -> HttpResponse:
    # minimal-view: no-logger-needed
    # return HttpResponse("Welcome to the Skincare Home Page!")
    return render(request, "home.html")


def product(request: HttpRequest) -> HttpResponse:
    # minimal-view: no-logger-needed
    # return HttpResponse("Product Ingredient Input Page")
    return render(request, "product.html")
