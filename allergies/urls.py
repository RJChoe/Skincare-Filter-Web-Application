from django.urls import path

from . import views

app_name = "allergies"

urlpatterns = [
    path("", views.allergy_list, name="list"),
    path("create/", views.create_allergies, name="create"),
    path("<int:pk>/edit/", views.edit_allergy, name="edit"),
    path("<int:pk>/delete/", views.delete_allergy, name="delete"),
]
