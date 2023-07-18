from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome_page, name="welcome_page"),
    path("getstarted", views.get_started, name="get_started"),
    path("posts", views.posts, name="posts"),
    path("about", views.about, name="about"),
    path("profile", views.profile, name="profile"),
    path("posts/<slug:slug>", views.post_content, name="post_content"),
    path("log-in", views.log_in, name="log_in"),
    path("<str:attemptedURL>", views.raise_404_error, name="404Error")
]

