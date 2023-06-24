from django.http import Http404
from django.shortcuts import render


# Create your views here.


def welcome_page(request):
    return render(request, "./main_app/welcome_page.html", {
        "page_title": "Welcome!"
    })


def get_started(request):
    return render(request, "./main_app/getStarted.html", {
        "page_title": "getStarted"
    })


def recent_posts(request):
    return render(request, "./main_app/recentPosts.html", {
        "page_title": "recentPosts"
    })


def about(request):
    return render(request, "./main_app/about.html", {
        "page_title": "about"
    })


def raise_404_error(request, attemptedURL):
    raise Http404(f"This page does not exist on CoderKai")
