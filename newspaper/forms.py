from django import forms
from django.forms.widgets import SelectDateWidget
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Newspaper, Topic

class SearchForm(forms.Form):
    search = forms.CharField(label='Search', required=False)


class FilterTopicForm(forms.Form):
    by_topic = forms.ChoiceField(
        choices=[('', 'All topics')] + [(topic.id, topic.name) for topic in Topic.objects.all()],
        required=False,
        initial='',
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class NewspaperCreateForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = "__all__"
        widgets = {
            'published_date': SelectDateWidget(),
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
