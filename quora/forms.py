from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User, Question, Answer


def validate_password_length(value):
    if len(value) < 5:
        raise ValidationError("Password must be at least 5 characters long.")
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        } 