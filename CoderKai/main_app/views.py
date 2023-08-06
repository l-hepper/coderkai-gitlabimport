from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin


from django.views.generic.edit import UpdateView
from main_app.forms import ProfileInfoForm, SignUpForm
from main_app.models import CoderKaiPoints, ProfileInfo


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


class HomepageView(TemplateView):
    template_name = "./main_app/welcome_page.html"


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


class ProfileView(View):
    template_name = "./main_app/profile.html"

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        print(f"logged in as {user.username}")  # for debugging
        return render(request, self.template_name, {'user': user})


class CompleteProfileView(LoginRequiredMixin, FormView):
    login_url = "login"
    template_name = "./main_app/complete_profile.html"
    form_class = ProfileInfoForm
    success_url = "profile"

    def form_valid(self, form):
        profileinfo = form.save(commit=False)
        profileinfo.user = self.request.user
        profileinfo.save()

        interests = self.request.POST.getlist('interests')
        motivations = self.request.POST.getlist('motivations')

        for interest in interests:
            profileinfo.interests.add(interest)

        for motivation in motivations:
            profileinfo.motivations.add(motivation)

        return super().form_valid(form)


class EditProfileView(UpdateView):
    model = ProfileInfo
    form_class = ProfileInfoForm
    template_name = "./main_app/edit_profile.html"
    success_url = reverse_lazy('profile')  # Assuming 'profile' is the name of the desired URL pattern


class SignUpView(FormView):
    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = "complete-profile"

    def form_valid(self, form):
        user = form.save()  # `form.save()` should return the user object
        login(self.request, user)  # Log the user in
        # create an instance of points for the user, starting at 0
        CoderKaiPoints.objects.create(user=self.request.user, points=0)
        return super().form_valid(form)


def raise_404_error(request, attemptedURL):
    raise Http404(f"This page does not exist on CoderKai")


def logout_view(request):
    print(f"logging out of {request.user}")  # for debugging
    logout(request)
    return render(request, "main_app/welcome_page.html")
