from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from .models import User
from .validators import validate_password_length

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        validators=[validate_password_length]
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        validators=[validate_password_length]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] 