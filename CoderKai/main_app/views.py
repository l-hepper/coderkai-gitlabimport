import re
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.views.generic.base import TemplateView

from django.views.generic.edit import UpdateView
from django.utils.html import escape
from main_app.forms import KaiGroupForm, NewPostForm, NewReplyForm, NewResponseForm, ProfileInfoForm, SignUpForm
from main_app.models import KaiGroup, Post, PostKudos, ProfileInfo, Reply, Response, ResponseKudos, TypeTag

# these are the factors which are taken into account when calculating recommendation scores for content to serve a user
INTEREST_MATCH_SCORE = 10
MOTIVATION_MATCH_SCORE = 5
INTRODUCTION_POST_BONUS = 10
RESPONSE_SCORE_FACTOR = 1

class HomepageView(View):
    template_name = "./main_app/welcome_page.html"

    def get(self, request):
        if request.user.is_authenticated:
            recommended_posts = self.recommendation_score(request.user)[::-1]
            posts = {}

            for post in recommended_posts:
                posts[post] = Response.objects.filter(post=post).count()

            groups = self.recommend_groups(request.user)

            return render(request, self.template_name, {
                'posts': posts,
                'group_list': groups,
            })
        else:
            return render(request, self.template_name)

    # this function is the algorithm that constructs the recommendation score for each post.
    def recommendation_score(self, user):

        # Filtering posts from the last week only
        one_week_ago = timezone.now() - timedelta(days=7)
        posts = Post.objects.filter(timestamp__gte=one_week_ago)

        user_profile = ProfileInfo.objects.get(user=user)
        user_interests = set(user_profile.interests.values_list('name', flat=True))
        user_motivations = set(user_profile.motivations.values_list('name', flat=True))

        post_scores = {}

        for post in posts:

            if post.author == user:
                continue

            score = 0
            post_tags = set(post.tags.values_list('name', flat=True))

            # recommendation score is increased if the post tags match the users interest and motivations
            score += len(post_tags.intersection(user_interests)) * INTEREST_MATCH_SCORE
            score += len(post_tags.intersection(user_motivations)) * MOTIVATION_MATCH_SCORE

            # posts with a higher kudos are given higher recommendation score
            score += post.kudos

            # posts with lots of responses are given a boost to recommendation score
            score += post.response.count() * RESPONSE_SCORE_FACTOR

            # introduction posts are boosted to welcome and support new users with similar interests
            if post.type_tag and post.type_tag.name == 'introduction':
                score += INTRODUCTION_POST_BONUS

            post_scores[post.id] = score

        # Sorting the posts by their scores
        recommended_posts = sorted(post_scores.keys(), key=lambda x: post_scores[x])

        # Return top 10 posts
        return Post.objects.filter(id__in=recommended_posts[-10:])

    def recommend_groups(self, user):
        user_profile = ProfileInfo.objects.get(user=user)
        user_interests = user_profile.interests.all()
        user_motivations = user_profile.motivations.all()

        # Filter groups based on user's interests and motivations
        # Annotate the groups with a score based on the number of matches
        # Order by this score and retrieve the top 3
        groups = (KaiGroup.objects
                  .filter(Q(interests__in=user_interests) | Q(motivations__in=user_motivations))
                  .annotate(match_score=Count('interests', distinct=True) + Count('motivations', distinct=True))
                  .order_by('-match_score')[:3])

        return groups

class CoderKaiGuideView(TemplateView):
    template_name = "./main_app/coderkai_guide.html"



class PostsView(View):
    template_name = "./main_app/posts.html"

    def get(self, request):
        
        post_list = Post.objects.all()

        # the default display options are 'filter=all' and 'sort=most_recent'
        sort_option = request.GET.get('sort', 'most_recent')
        filter_option = request.GET.get('filter', 'all')

        #sorting options
        if sort_option == 'most_recent':
            post_list = post_list.order_by('-timestamp')
        elif sort_option == 'most_active':
            post_list = post_list.annotate(reply_count=Count('response')).order_by('-reply_count')
        elif sort_option == 'most_kudosed':
            post_list = post_list.order_by('-coderkaipoints')

        #filtering options
        if filter_option == 'all':
            post_list = post_list.all()
        elif filter_option == 'unanswered_only':
            post_list = post_list.annotate(num_responses=Count('response')).filter(num_responses=0)
        elif filter_option == 'introduction_only':
            post_list = post_list.filter(type_tag__name="Introduction")
        elif filter_option == 'question_only':
            post_list = post_list.filter(type_tag__name="Question")
        elif filter_option == 'discussion_only':
            post_list = post_list.filter(type_tag__name="Discussion")

        # pagination improves query efficiency and usability of the 'posts' page
        paginator = Paginator(post_list, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)

        post_info = {}
        for post in posts:
            post_info[post] = Response.objects.filter(post=post).count()

        return render(request, self.template_name, {
            'posts': post_info,
            'posts_pag': posts,  # required for page navigation/pagination
            'sort_option': sort_option.replace('_', ' '),
            'filter_option': filter_option.replace('_', ' ')
        })


class PostContent(View):
    template_name = "./main_app/post_content.html"

    def get(self, request, **kwargs):

        try:
            post = Post.objects.get(slug=kwargs['slug'])
        except Post.DoesNotExist:
            raise Http404("Post does not exist")

        responses = Response.objects.filter(post=post).order_by("-timestamp")
        response_dictionary = {}

        for response in responses:
            response_dictionary[response] = Reply.objects.filter(
                response=response)

        return render(request, self.template_name, {
            'post': post,
            'no_responses': len(responses),
            'response_dictionary': response_dictionary,
            'response_dict_length': len(response_dictionary)
        })


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
        post.kudos += 1
        post.save()
        return JsonResponse({'post_id': post.id, 'kudos': post.kudos})


class AllGroupsView(View):
    template_name = "./main_app/all_groups.html"

    def get(self, request):
        group_list = KaiGroup.objects.all().order_by('-created_at')

        # paginator = Paginator(post_list, 10)
        # page = request.GET.get('page')
        # posts = paginator.get_page(page)

        # post_info = {}
        # for post in posts:
        #     post_info[post] = Response.objects.filter(post=post).count()

        return render(request, self.template_name, {
            'group_list': group_list
        })


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
        response.kudos += 1
        response.save()
        return JsonResponse({'response_id': response.id, 'kudos': response.kudos})


def about(request):
    return render(request, "./main_app/about.html", {
        "page_title": "About"
    })


class ProfileView(LoginRequiredMixin, View):
    login_url = "login"
    template_name = "./main_app/profile.html"

    def get(self, request, **kwargs):
        user = User.objects.get(username=kwargs['username'])
        num_of_questions = Post.objects.filter(author=user).count()

        users_answers = Response.objects.filter(author=user).order_by('-kudos')
        num_of_answers = users_answers.count()
        top3_answers = users_answers[:3]

        post_kudos = Post.objects.filter(author=user).aggregate(total=Sum('kudos'))['total'] or 0
        response_kudos = Response.objects.filter(author=user).aggregate(total=Sum('kudos'))['total'] or 0

        user.profileinfo.kudos = post_kudos + response_kudos + 1
        user.profileinfo.save()

        self.set_rank(user.profileinfo.kudos, user)

        return render(request, self.template_name, {
            'profileinfo': user,
            'num_of_questions': num_of_questions,
            'num_of_answers': num_of_answers,
            'top3_answers': top3_answers,
        })
    
    def set_rank(self, total_kudos, user):
        if total_kudos > 499:
            user.profileinfo.rank = "Cyber Sensei"
        elif total_kudos > 399:
            user.profileinfo.rank = "Digital Druid"
        elif total_kudos > 299:
            user.profileinfo.rank = "Logic Lancer"
        elif total_kudos > 199:
            user.profileinfo.rank = "Kernel Knight"
        elif total_kudos > 99:
            user.profileinfo.rank = "Bit Brigadier"
        else:
            user.profileinfo.rank = "Code Cadet"
        
        user.profileinfo.save()
    



class CompleteProfileView(LoginRequiredMixin, FormView):
    login_url = "login"
    template_name = "./main_app/complete_profile.html"
    form_class = ProfileInfoForm
    success_url = reverse_lazy('welcome_page')

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

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})


class SignUpView(FormView):
    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = "complete-profile"

    def form_valid(self, form):
        user = form.save()  # `form.save()` should return the user object
        login(self.request, user)  # Log the user in
        return super().form_valid(form)


class NewPostView(LoginRequiredMixin, FormView):
    login_url = "login"
    template_name = './main_app/new_post.html'
    form_class = NewPostForm
    success_url = "posts"  # TODO-will be changed to the actual post view

    def form_valid(self, form):
        post = form.save(commit=False)

        post.author = self.request.user
        post.author.profileinfo.kudos += 1
        post.kudos = 1
        post.slug = slugify(post.title)[:49]

        preview_body = re.sub('\[coderkai!\].*?\[/coderkai!\]', '[CODEBLOCK]', post.body, flags=re.DOTALL)
        post.preview = preview_body[0:498] + "..."

        post.body = escape(post.body)
        post.body = post.body.replace('[coderkai!]', '<pre><code>')
        post.body = post.body.replace('[/coderkai!]', '</code></pre>')



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

        response.body = escape(response.body)
        response.body = response.body.replace('[coderkai!]', '<pre><code>')
        response.body = response.body.replace('[/coderkai!]', '</code></pre>')


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


def custom_404(request, exception):
    context = {
        'error_message': 'Coder Kai is unable to find this page!'
    }
    print("CALLED custom 404") # for debugging

    if 'user' in request.path:
        context['error_message'] = 'User not found.'
    elif 'posts' in request.path:
        context['error_message'] = 'This post does not exist on Coder Kai'
    elif 'group' in request.path:
        context['error_message'] = 'This group does not exist on Coder Kai'

    return render(request, "./main_app/404.html", context)


def logout_view(request):
    print(f"logging out of {request.user}")  # for debugging
    logout(request)
    return render(request, "main_app/welcome_page.html")


class CreateKaiGroupView(LoginRequiredMixin, FormView):
    template_name = './main_app/create_kaigroup.html'
    form_class = KaiGroupForm

    def form_valid(self, form):
        self.groupform = form.save(commit=False)
        self.groupform.slug = slugify(self.groupform.name)
        self.groupform.creator = self.request.user
        self.groupform.save()

        form.save_m2m()

        self.groupform.members.add(self.groupform.creator)

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('kaigroup', kwargs={'slug': self.groupform.slug})


class KaiGroupView(View):
    template_name = "./main_app/kaigroup.html"

    def get(self, request, **kwargs):
        group = KaiGroup.objects.get(slug=kwargs['slug'])

        member_list = group.members.all()
        group_kudos = 0

        for member in member_list:
            member_kudos = member.profileinfo.kudos
            group_kudos += member_kudos

        most_kudosed_members = group.members.annotate(kudos_value=F('profileinfo__kudos')).order_by('-kudos_value')[:6]

        return render(request, self.template_name, {
            'group': group,
            'group_kudos': group_kudos,
            'most_kudosed_members': most_kudosed_members
        })
    
class EditGroupView(UpdateView):
    model = KaiGroup
    form_class = KaiGroupForm
    template_name = "./main_app/edit_group.html"

    def get_success_url(self):
        return reverse('kaigroup', kwargs={'slug': self.object.slug})


class JoinGroupView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        group = KaiGroup.objects.get(name=kwargs['groupname'])

        # Check if user already kudosed this post or if they're the author
        group.members.add(request.user)

        # If checks pass, create a vote record and update post kudos.
        return HttpResponseRedirect(reverse("kaigroup", kwargs={'slug': group.slug}))


class LeaveGroupView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        group = KaiGroup.objects.get(name=kwargs['groupname'])

        # Check if user already kudosed this post or if they're the author
        group.members.remove(request.user)

        # If checks pass, create a vote record and update post kudos.
        return HttpResponseRedirect(reverse("kaigroup", kwargs={'slug': group.slug}))
    

class EditPostView(UpdateView):
    model = Post
    form_class = NewPostForm
    template_name = "./main_app/edit_post.html"

    def get_success_url(self):
        return reverse('post_content', kwargs={'slug': self.object.slug})
    

class EditResponseView(UpdateView):
    model = Response
    form_class = NewResponseForm
    template_name = "./main_app/edit_response.html"

    def get_success_url(self):
        return reverse('post_content', kwargs={'slug': self.object.post.slug })

