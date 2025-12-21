from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Create your views here.
def user_list(request: HttpRequest) -> HttpResponse:
    return render(request, "user/user_list.html")
