from django.test import TestCase
from django.contrib.auth.models import User

from .models import Post, Tag, TypeTag, ProfileInfo, Interest, Motivation, KaiGroup, Response, Reply
from django.urls import reverse


class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', email='test.user@example.com', password='testpassword123')

        self.tag = Tag.objects.create(name='Coding Basics')
        self.type_tag = TypeTag.objects.create(name='Test Data')

        self.post = Post.objects.create(
            author=self.user,
            title='Learning to Code',
            body="Start with understanding the basics",
            preview='A beginner guide to coding basics.',
            slug='learning-to-code',
            kudos=3,
        )
        self.post.tags.add(self.tag)
        self.post.type_tag = self.type_tag
        self.post.save()

    def test_post_creation(self):
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post.author.username, 'test_user')
        self.assertEqual(self.post.title, 'Learning to Code')
        self.assertIn(self.tag, self.post.tags.all())
        self.assertEqual(self.post.type_tag, self.type_tag)
        self.assertEqual(self.post.kudos, 3)

    def test_post_slug(self):
        self.assertEqual(self.post.slug, 'learning-to-code')

    def test_post_preview(self):
        self.assertEqual(self.post.preview,
                         'A beginner guide to coding basics.')


class ProfileInfoTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', email='test.user@example.com', password='testpassword123')

        self.interest = Interest.objects.create(name='Python')
        self.motivation = Motivation.objects.create(name='Academic')

        self.profile = ProfileInfo.objects.create(
            user=self.user,
            about_me="Beginner in coding",
            kudos=2,
            rank="Code Cadet"
        )
        self.profile.interests.add(self.interest)
        self.profile.motivations.add(self.motivation)

    def test_profile_creation(self):
        self.assertEqual(ProfileInfo.objects.count(), 1)
        self.assertEqual(self.profile.user.username, 'test_user')
        self.assertEqual(self.profile.about_me,
                         "Beginner in coding")
        self.assertIn(self.interest, self.profile.interests.all())
        self.assertIn(self.motivation, self.profile.motivations.all())

    def test_default_values(self):
        self.assertEqual(self.profile.kudos, 2)
        self.assertEqual(self.profile.rank, "Code Cadet")


class KaiGroupTestCase(TestCase):

    def setUp(self):
        self.creator = User.objects.create_user(username='creator_user', email='creator.user@example.com', password='testpassword123')
        self.member = User.objects.create_user(username='member_user', email='member.user@example.com', password='testpassword123')
        
        self.interest = Interest.objects.create(name='Python')
        self.motivation = Motivation.objects.create(name='Academic')

        self.group = KaiGroup.objects.create(
            name='Code Learners',
            about="A group about learning to code.",
            creator=self.creator,
            slug='code-learners'
        )
        self.group.members.add(self.member)
        self.group.interests.add(self.interest)
        self.group.motivations.add(self.motivation)

    def test_kaigroup_creation(self):
        self.assertEqual(KaiGroup.objects.count(), 1)
        self.assertEqual(self.group.name, 'Code Learners')
        self.assertEqual(self.group.about, "A group about learning to code.")
        self.assertEqual(self.group.creator, self.creator)
        self.assertIn(self.member, self.group.members.all())
        self.assertIn(self.interest, self.group.interests.all())
        self.assertIn(self.motivation, self.group.motivations.all())

    def test_slug(self):
        self.assertEqual(self.group.slug, 'code-learners')

    def test_default_group_image(self):
        self.assertEqual(self.group.group_image, "images/default-avatar.png")


class HomepageViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password123')
        self.url = reverse('welcome_page')

    def test_unauthenticated_user_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './main_app/welcome_page.html')


class PostContentTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password123')
        
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            body='This is a test post',
            slug='test-post'
        )

        self.response = Response.objects.create(
            post=self.post,
            author=self.user,
            body='This is a response to the test post'
        )

        self.reply = Reply.objects.create(
            response=self.response,
            author=self.user,
            body='This is a reply to the response'
        )

        self.url = reverse('post_content', kwargs={'slug': 'test-post'})
        self.invalid_url = reverse('post_content', kwargs={'slug': 'invalid-slug'})

    def test_existing_post_slug(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './main_app/post_content.html')
        self.assertEqual(response.context['post'], self.post)
        self.assertEqual(response.context['no_responses'], 1)
        self.assertEqual(len(response.context['response_dictionary']), 1)

    def test_responses_and_replies(self):
        response = self.client.get(self.url)
        self.assertIn(self.response, response.context['response_dictionary'])
        replies = response.context['response_dictionary'][self.response]
        self.assertIn(self.reply, replies)

