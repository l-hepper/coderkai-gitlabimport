from django.shortcuts import render


# Create your views here.

def welcome_page(request):
    return render(request, "./main_app/welcome_page.html")


def user_profile(request):
    return render(request, "./main_app/user_profile.html")
