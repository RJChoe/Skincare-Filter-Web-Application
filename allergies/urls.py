from django.urls import path

from . import views

app_name = "allergies"

urlpatterns = [
    path("", views.allergies_list, name="list"),
]
