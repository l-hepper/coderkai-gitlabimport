from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome_page, name="welcome-page"),
    path("user-profile", views.user_profile, name="user-profile"),
    path("posts", views.posts, name="posts"),
    path("about", views.about, name="about"),
    path("<str:attemptedURL>", views.raise_404_error, name="404Error")
]
