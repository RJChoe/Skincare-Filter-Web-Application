from django.urls import path

from . import views

urlpatterns = [
    path("", views.allergies_list, name="allergy_list"),
]
