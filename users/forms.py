from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserRegistrationForm(UserCreationForm):

    username = forms.EmailField(required= True)
    username.label = "Email"

    """
    Override to give customized error message.
    """
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Email already exists")
        return username



