from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.user_list, name='list'),     # -> /users/
    path('<int:pk>/', views.user_detail, name='detail'),  # -> /users/42/
]