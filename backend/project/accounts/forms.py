from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
