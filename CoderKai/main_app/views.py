from django.http import Http404
from django.shortcuts import render


# Create your views here.

post_dictionary = {
     "post-01": {
        "post_title": "How do I convert a DataFrame to a dictionary using pandas?",
        "post_preview": "Bro ipsum dolor sit amet bowl brain bucket T-Bar...",
        "post_replies": "5",
        "post_author": "SuperCoder77",
        "post_time" : "26/06/2023 16:21"
    },
    "post-02": {
        "post_title": "CODE REVIEW: Please review my code for improvements and better design.",
        "post_preview": "Please see my code below and tell me if there are improvements to be made",
        "post_replies": "1",
        "post_author": "TotalNoob99",
        "post_time": "21/06/2023 12:31"
    },
    "post-03": {
        "post_title": "What's the best way to learn Python for data science?",
        "post_preview": "Hey guys, I'm looking for recommendations on resources for learning Python...",
        "post_replies": "7",
        "post_author": "DataEnthusiast21",
        "post_time" : "20/06/2023 17:43"
    },
    "post-04": {
        "post_title": "Need help with a SQL query",
        "post_preview": "I have a complex SQL query that I'm struggling with. Can anyone help...",
        "post_replies": "3",
        "post_author": "DBMaster",
        "post_time": "19/06/2023 10:56"
    },
    "post-05": {
        "post_title": "Looking for advice on web app security",
        "post_preview": "Developing a web app and want to ensure it's secure. What practices should I follow...",
        "post_replies": "6",
        "post_author": "SecuritySam",
        "post_time": "18/06/2023 18:05"
    },
    "post-06": {
        "post_title": "Challenges in Machine Learning",
        "post_preview": "Discussing the current challenges in machine learning and possible solutions...",
        "post_replies": "4",
        "post_author": "MLGuru",
        "post_time": "17/06/2023 15:11"
    },
    "post-07": {
        "post_title": "Can anyone explain REST APIs in simple terms?",
        "post_preview": "I'm a beginner and struggling to understand REST APIs. Could use a simple explanation...",
        "post_replies": "8",
        "post_author": "Newbie101",
        "post_time": "16/06/2023 13:25"
    },
    "post-08": {
        "post_title": "How to optimize JavaScript performance in large scale applications",
        "post_preview": "Share tips and tricks to boost JavaScript performance in large scale applications...",
        "post_replies": "2",
        "post_author": "JavaScriptJedi",
        "post_time": "15/06/2023 09:33"
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
        "posts" : post_dictionary
    })


def post_content(request, slug):
    return render(request, "./main_app/post_content.html", {
        "page_title": "Post Content",
    })

def about(request):
    return render(request, "./main_app/about.html", {
        "page_title": "About"
    })


def raise_404_error(request, attemptedURL):
    raise Http404(f"This page does not exist on CoderKai")
