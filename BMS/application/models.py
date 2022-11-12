from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .validators import schoolEmailValidator



MAX_NAME_LENGTH = 30

# the custom user doesn't have a username field, but uses the email as unique identifier
class User(AbstractUser):
    name = models.TextField(max_length=MAX_NAME_LENGTH, help_text="Preferred name")
    # set email field as unique
    email = models.EmailField(
        _('email address'), 
        unique=True, 
        validators=[schoolEmailValidator], 
        error_messages={
            "unique": _("A user with that email already exists.")
        }
    )

    # remove the username field from abstract user
    username = None

    # redefine standard fields as email
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    



    
