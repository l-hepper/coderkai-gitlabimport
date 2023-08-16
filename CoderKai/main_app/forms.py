from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from main_app.models import Interest, KaiGroup, Motivation, Post, ProfileInfo, Reply, Response, Tag, TypeTag


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    # Required to change the label of password2 to "Confirm Password"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].label = "Confirm password"


class ProfileInfoForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), widget=forms.CheckboxSelectMultiple)
    motivations = forms.ModelMultipleChoiceField(queryset=Motivation.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = ProfileInfo
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(ProfileInfoForm, self).__init__(*args, **kwargs)
        self.fields['interests'].help_text = 'Choose your areas of study and focus!'
        self.fields['motivations'].help_text = 'Select why you are learning to code!'


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileInfo
        exclude = ['user']


class NewPostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)
    type_tag = forms.ModelChoiceField(queryset=TypeTag.objects.all())


    class Meta:
        model = Post
        fields = ['type_tag', 'title', 'body', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = "Post body:"
        self.fields['type_tag'].label = "Post type:"
        self.fields['body'].help_text = "Keep it clean, concise, and positive. That's Coder Kai!"
        self.fields['tags'].help_text = "Pin your post with the relevant tags to promote engagement!"


class NewResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = "Enter your answer below:"
        self.fields['body'].help_text = "Your answer should be clear, concise, and positive. That's Coder Kai!"


class NewReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = "Enter your reply below:"
        self.fields['body'].help_text = "Replies are used to thank people or ask for more information on their answer."


class KaiGroupForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), widget=forms.CheckboxSelectMultiple)
    motivations = forms.ModelMultipleChoiceField(queryset=Motivation.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = KaiGroup
        fields = ['name', 'about', 'interests', 'motivations']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)