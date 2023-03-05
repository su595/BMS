from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.timezone import now
from django.db.models import Q

from .validators import schoolEmailValidator
from .models import Bike, Borrowing, User

# custom RegisterForm with hidden, automatic "username" field
class RegisterForm(UserCreationForm):

    # make email field with appropriate validators
    email = forms.EmailField(label="Email", help_text="Must be a school email.", validators=[schoolEmailValidator])
    # username field is hidden and not required, because in clean I automatically set it to the "email stem"
    username = UsernameField(widget=forms.HiddenInput(), required=False)


    def clean(self):
        super().clean()

        # set the username as email stem (what comes before the @)
        email_stem, domain = self.cleaned_data["email"].split("@")
        self.cleaned_data["username"] = email_stem

        return self.cleaned_data

    class Meta:
        model = get_user_model()
        fields = ( "email", "first_name", 'password1', "password2", "username")


class LoginForm(AuthenticationForm):
    # custom LoginForm that changes the label of the username field
    username = forms.CharField(label='Email')


class BikeCreationForm(forms.ModelForm):

    # the steward must have own_bike permission
    steward = forms.ModelChoiceField(queryset=User.objects.filter(
        Q(is_superuser=True) |
        Q(user_permissions__codename="own_bike") |
        Q(groups__permissions__codename="own_bike")).distinct()
        )
    
    class Meta:
        model = Bike
        fields = ["number", "steward", "size"]


class BorrowingCreationForm(forms.Form):

    # i only need the endtime, everything else is determined programatically
    end_time = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], required=True)

    class Meta:
        model = Borrowing
        fields = ["end_time",]


class ChangeUserForm(forms.ModelForm):       

    groups = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = get_user_model()
        fields = ["first_name", "groups"]

