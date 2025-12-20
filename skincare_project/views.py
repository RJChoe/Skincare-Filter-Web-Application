from django.shortcuts import render

# functions for rendering pages -processing requests and returning responses
# database, cache, HTML templates, etc. can be integrated here


def home(request):
    # return HttpResponse("Welcome to the Skincare Home Page!")
    return render(request, "home.html")


def product(request):
    # return HttpResponse("Product Ingredient Input Page")
    return render(request, "product.html")
