from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.HomepageView.as_view(), name="welcome_page"),
    path("getstarted", views.get_started, name="get_started"),
    path("posts", views.PostsView.as_view(), name="posts"),
    path("about", views.about, name="about"),
    path("profile", views.ProfileView.as_view(), name="profile"),
    path("complete-profile", views.CompleteProfileView.as_view(), name="complete_profile"),
    path("edit-profile/<int:pk>", views.EditProfileView.as_view(), name="edit_profile"),
    path("posts/<slug:slug>", views.PostContent.as_view(), name="post_content"),
    path("new-post", views.NewPostView.as_view(), name="new_post"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("logout", views.logout_view, name="logout"),
    path("<str:attemptedURL>", views.raise_404_error, name="404Error")
]

