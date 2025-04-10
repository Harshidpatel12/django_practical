from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Question, Answer



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }
