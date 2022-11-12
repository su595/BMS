# custom validators

from django.core.exceptions import ValidationError


# add more validation to this function later
def schoolEmailValidator(email):

    if "@uwcrobertboschcollege.de" not in email:
        raise ValidationError(
            "The email isn't a school email :(",
            code='bad_email',
        )
    return email


