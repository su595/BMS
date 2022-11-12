from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _
from .validators import schoolEmailValidator


# custom RegisterForm without the "username" field
class RegisterForm(UserCreationForm):

    name = forms.CharField(label="Preferred name")
    # make email field with appropriate validators
    email = forms.EmailField(label="Email", help_text="Must be a school email.", validators=[schoolEmailValidator])


    class Meta:
        model = get_user_model()
        fields = ( "email", "name", 'password1', "password2")


# custom LoginForm that changes the label of the username field
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')