from itertools import count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from datetime import datetime
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


from django.views.generic.edit import UpdateView
from main_app.forms import NewPostForm, NewReplyForm, NewResponseForm, ProfileInfoForm, SignUpForm
from main_app.models import CoderKaiPoints, Post, PostKudos, ProfileInfo, Reply, Response, ResponseKudos, TypeTag


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
        post_list = Post.objects.all().order_by('-timestamp')
        post_info = {}

        for post in post_list:
            post_info[post] = Response.objects.filter(post=post).count()

        return render(request, self.template_name, {
            'posts': post_info
        })


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
        responses = Response.objects.filter(post=post).order_by("-timestamp")
        response_dictionary = {}

        for response in responses:
            response_dictionary[response] = Reply.objects.filter(response=response)

        return render(request, self.template_name, {
            'post': post,
            'no_responses': len(responses),
            'response_dictionary': response_dictionary
        })


# class KudosPostView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         post_id = self.kwargs['post_id']
#         post = Post.objects.get(pk=post_id)
#         post.coderkaipoints += 1
#         post.save()
#         return JsonResponse({'post_id': post.id, 'coderkaipoints': post.coderkaipoints})

class KudosPostView(View):
    
    def post(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        
        # Check if user already kudosed this post or if they're the author
        if PostKudos.objects.filter(user=request.user, post=post).exists():
            return JsonResponse({'error': "You kudosed this post already!"}, status=400)
        
        if post.author == request.user:
            return JsonResponse({'error': 'Sorry, no giving yourself kudos!'}, status=400)

        # If checks pass, create a vote record and update post kudos.
        PostKudos.objects.create(user=request.user, post=post)
        post.coderkaipoints += 1
        post.save()
        return JsonResponse({'post_id': post.id, 'coderkaipoints': post.coderkaipoints})
    

class KudosResponseView(View):
    
    def post(self, request, *args, **kwargs):
        response_id = kwargs['response_id']
        response = Response.objects.get(pk=response_id)
        
        if ResponseKudos.objects.filter(user=request.user, response=response).exists():
            return JsonResponse({'error': "You kudosed this response already!"}, status=400)
        
        if response.author == request.user:
            return JsonResponse({'error': 'Sorry, no giving yourself kudos!'}, status=400)

        # If checks pass, create a vote record and update post kudos.
        ResponseKudos.objects.create(user=request.user, response=response)
        response.coderkaipoints += 1
        response.save()
        return JsonResponse({'response_id': response.id, 'coderkaipoints': response.coderkaipoints})


def about(request):
    return render(request, "./main_app/about.html", {
        "page_title": "About"
    })


class ProfileView(LoginRequiredMixin, View):
    login_url = "login"
    template_name = "./main_app/profile.html"

    def get(self, request, **kwargs):
        profile_info = User.objects.get(username=kwargs['username'])

        print(f"logged in as {self.request.user}")  # for debugging

        return render(request, self.template_name, {'profileinfo': profile_info})


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
        post.coderkaipoints = 1
        post.slug = slugify(post.title)
        post.preview = post.body[0:500] + "..."
        post.save()

        tags = self.request.POST.getlist('tags')
        for tag in tags:
            post.tags.add(tag)

        return super().form_valid(form)


class NewResponseView(LoginRequiredMixin, FormView):
    login_url = "login"
    template_name = './main_app/new_response.html'
    form_class = NewResponseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(slug=self.kwargs['slug'])
        context['post'] = post
        return context

    def form_valid(self, form):
        response = form.save(commit=False)

        post = Post.objects.get(slug=self.kwargs['slug'])
        response.post = post
        response.author = self.request.user

        response.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_content', kwargs={'slug': self.kwargs['slug']})


class NewReplyView(LoginRequiredMixin, FormView):
    login_url = "login"
    template_name = './main_app/new_reply.html'
    form_class = NewReplyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = Response.objects.get(id=self.kwargs['response_id'])
        context['response'] = response
        return context

    def form_valid(self, form):
        reply = form.save(commit=False)

        response = Response.objects.get(id=self.kwargs['response_id'])
        reply.response = response
        reply.author = self.request.user

        reply.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_content', kwargs={'slug': self.kwargs['slug']})


def raise_404_error(request, attemptedURL):
    raise Http404(f"This page does not exist on CoderKai")


def logout_view(request):
    print(f"logging out of {request.user}")  # for debugging
    logout(request)
    return render(request, "main_app/welcome_page.html")
