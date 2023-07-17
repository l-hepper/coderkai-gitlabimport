from django.http import Http404
from django.shortcuts import render
from datetime import datetime


# Create your views here.

post_dictionary = {
    "post-01": {
        "post_title": "How do I convert a DataFrame to a dictionary using pandas?",
        "post_preview": "Bro ipsum dolor sit amet bowl brain bucket T-Bar...",
        "post_replies": "5",
        "post_author": "SuperCoder77",
        "post_time": datetime.now()
    },
    "post-02": {
        "post_title": "CODE REVIEW: Please review my code for improvements and better design.",
        "post_preview": "Please see my code below and tell me if there are improvements to be made",
        "post_replies": "1",
        "post_author": "TotalNoob99",
        "post_time": datetime.now()
    },
    "post-03": {
        "post_title": "What's the best way to learn Python for data science?",
        "post_preview": "Hey guys, I'm looking for recommendations on resources for learning Python...",
        "post_replies": "7",
        "post_author": "DataEnthusiast21",
        "post_time": datetime.now()
    },
    "post-04": {
        "post_title": "Need help with a SQL query",
        "post_preview": "I have a complex SQL query that I'm struggling with. Can anyone help...",
        "post_replies": "3",
        "post_author": "DBMaster",
        "post_time": datetime.now()
    },
    "post-05": {
        "post_title": "Looking for advice on web app security",
        "post_preview": "Developing a web app and want to ensure it's secure. What practices should I follow...",
        "post_replies": "6",
        "post_author": "SecuritySam",
        "post_time": datetime.now()
    },
    "post-06": {
        "post_title": "Challenges in Machine Learning",
        "post_preview": "Discussing the current challenges in machine learning and possible solutions...",
        "post_replies": "4",
        "post_author": "MLGuru",
        "post_time": datetime.now()
    },
    "post-07": {
        "post_title": "Can anyone explain REST APIs in simple terms?",
        "post_preview": "I'm a beginner and struggling to understand REST APIs. Could use a simple explanation...",
        "post_replies": "8",
        "post_author": "Newbie101",
        "post_time": datetime.now()
    },
    "post-08": {
        "post_title": "How to optimize JavaScript performance in large scale applications",
        "post_preview": "Share tips and tricks to boost JavaScript performance in large scale applications...",
        "post_replies": "2",
        "post_author": "JavaScriptJedi",
        "post_time": datetime.now()
    },
    "post-09": {
        "post_title": "Guide to effective logging in applications",
        "post_preview": "Explore how to do effective logging in your applications to help with debugging and traceability...",
        "post_replies": "3",
        "post_author": "DevOpsDude",
        "post_time": datetime.now()
    },
    "post-10": {
        "post_title": "Debugging multithreaded applications in C++",
        "post_preview": "Looking for strategies and tips for debugging multithreaded C++ applications...",
        "post_replies": "5",
        "post_author": "CppConqueror",
        "post_time": datetime.now()
    },
    "post-11": {
        "post_title": "Exploring functional programming in JavaScript",
        "post_preview": "Discussion about how to leverage functional programming paradigms in JavaScript...",
        "post_replies": "7",
        "post_author": "FuncJS",
        "post_time": datetime.now()
    }
}


def welcome_page(request):
    return render(request, "./main_app/welcome_page.html", {
        "page_title": "Welcome!"
    })


def get_started(request):
    return render(request, "./main_app/get_started.html", {
        "page_title": "Get Started"
    })


def posts(request):
    return render(request, "./main_app/posts.html", {
        "page_title": "All Posts",
        "posts": post_dictionary
    })


def post_content(request, slug):
    clicked_post = post_dictionary[slug]
    return render(request, "./main_app/post_content.html", {
        "page_title": slug,
        "post_content": clicked_post
    })


def about(request):
    return render(request, "./main_app/about.html", {
        "page_title": "About"
    })


def raise_404_error(request, attemptedURL):
    raise Http404(f"This page does not exist on CoderKai")


