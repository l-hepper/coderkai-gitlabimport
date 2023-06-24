from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome_page, name="welcome-page"),
    path("getStarted", views.get_started, name="getStarted"),
    path("recentPosts", views.recent_posts, name="recentPosts"),
    path("about", views.about, name="about"),
    path("<str:attemptedURL>", views.raise_404_error, name="404Error")
]

