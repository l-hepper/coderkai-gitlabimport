from django.http import Http404
from django.shortcuts import render


# Create your views here.


def welcome_page(request):
    return render(request, "./main_app/welcome_page.html", {
        "page_title": "Welcome!"
    })


def user_profile(request):
    return render(request, "./main_app/user_profile.html", {
        "page_title": "UserProfile"
    })


def posts(request):
    return render(request, "./main_app/posts.html", {
        "page_title": "Posts"
    })


def about(request):
    return render(request, "./main_app/about.html", {
        "page_title": "About"
    })


def raise_404_error(request, attemptedURL):
    raise Http404(f"This page does not exist on CoderKai")
