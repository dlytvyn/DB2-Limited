import unicodedata
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from accounts.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Invalid credentials or user is not activated')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'birthday',
            'country',
            'city',
            'avatar'
        ]

        def check_email(self):
            email = self.cleaned_data.get('email')
            email_to_check = User.objects.filter(email=email)
            if email_to_check.exists():
                raise forms.ValidationError('This email has already registered!')
            return email

