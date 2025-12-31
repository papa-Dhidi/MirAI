from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    """
    A custom user creation form that includes an email field.
    """
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')
