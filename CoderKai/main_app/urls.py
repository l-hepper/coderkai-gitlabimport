from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome_page, name="welcome-page"),
    path("user-profile", views.user_profile, name="user-profile")
]
