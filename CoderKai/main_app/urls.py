from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.HomepageView.as_view(), name="welcome_page"),
    path("getstarted", views.get_started, name="get_started"),
    path("posts", views.posts, name="posts"),
    path("about", views.about, name="about"),
    path("profile", views.profile, name="profile"),
    path("posts/<slug:slug>", views.post_content, name="post_content"),
    path('login', auth_views.LoginView.as_view(template_name='main_app/log_in.html'), name='log_in'),
    path("<str:attemptedURL>", views.raise_404_error, name="404Error")
]

