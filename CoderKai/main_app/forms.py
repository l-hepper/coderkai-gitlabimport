from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from main_app.models import Interest, Motivation, Post, ProfileInfo


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
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(), widget=forms.CheckboxSelectMultiple)
    motivations = forms.ModelMultipleChoiceField(
        queryset=Motivation.objects.all(), widget=forms.CheckboxSelectMultiple)

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
    class Meta:
        model = Post
        fields = ['title', 'body']