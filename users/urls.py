from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("", views.user_list, name="list"),  # maps to /users/ (app root)
    path("profile/", views.profile, name="profile"),
]
