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
from django.utils.text import slugify


from django.views.generic.edit import UpdateView
from main_app.forms import NewPostForm, ProfileInfoForm, SignUpForm
from main_app.models import CoderKaiPoints, Post, ProfileInfo


# Create your views here.


class HomepageView(TemplateView):
    template_name = "./main_app/welcome_page.html"


def get_started(request):
    return render(request, "./main_app/get_started.html", {
        "page_title": "Get Started"
    })


# def posts(request):
#     return render(request, "./main_app/posts.html", {
#         "page_title": "All Posts",
#         "posts": post_dictionary
#     })


class PostsView(View):
    template_name = "./main_app/posts.html"

    def get(self, request):
        posts = Post.objects.all().order_by('-timestamp')
        return render(request, self.template_name, {'posts': posts})


# def post_content(request, slug):
#     clicked_post = post_dictionary[slug]
#     return render(request, "./main_app/post_content.html", {
#         "page_title": slug,
#         "post_content": clicked_post
#     })

class PostContent(View):
    template_name = "./main_app/post_content.html"

    def get(self, request, **kwargs):
        post = Post.objects.get(slug=kwargs['slug'])
        return render(request, self.template_name, {'post': post})


def about(request):
    return render(request, "./main_app/about.html", {
        "page_title": "About"
    })


class ProfileView(LoginRequiredMixin, View):
    login_url = "login"
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
    # Assuming 'profile' is the name of the desired URL pattern
    success_url = reverse_lazy('profile')


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


class NewPostView(LoginRequiredMixin, FormView):
    login_url = "login"
    template_name = './main_app/new_post.html'
    form_class = NewPostForm
    success_url = "posts"  # TODO-will be changed to the actual post view

    def form_valid(self, form):
        post = form.save(commit=False)

        post.author = self.request.user
        post.coderkaipoints = 1  # or calculate this value somehow
        post.slug = slugify(post.title)  # you will need to import slugify
        post.preview = post.body[0:500] + "..."

        post.save()
        
        tags = self.request.POST.getlist('tags')
        for tag in tags:
            post.tags.add(tag)

        return super().form_valid(form)


def raise_404_error(request, attemptedURL):
    raise Http404(f"This page does not exist on CoderKai")


def logout_view(request):
    print(f"logging out of {request.user}")  # for debugging
    logout(request)
    return render(request, "main_app/welcome_page.html")
