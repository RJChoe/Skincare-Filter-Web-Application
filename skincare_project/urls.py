"""
URL configuration for skincare_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('users/', include(('user.urls', 'user'), namespace='user')),
    path('product/', views.product, name='product'),
]

#TO DO:
#Add names to your URL patterns for better maintainability.
#For example, change path('', views.home) to path('', views.home, name='home').

#Use named URLs in templates instead of hard-coded paths (e.g., change <a href="/user"> to <a href="{% url 'user' %}">) after you give that route a name.
#Add a small test that asserts reverse('home') == '/' if you set name='home' in your URLconf.,