# custom validators

from django.core.exceptions import ValidationError


# add more validation to this function later
def schoolEmailValidator(email):

    # if the domain of the email isn't the school domain
    if "@uwcrobertboschcollege.de" not in email:
        raise ValidationError(
            "The email isn't a school email :(",
            code='bad_email',
        )

    return email


def bikeSizeValidator(size):

    # if size isn't exactly s,m or l (case-insensitive)
    if size.upper() == "S" or size.upper() == "M" or size.upper() == "L":
        return size.upper()
            
    raise ValidationError(
        "not correct size :("
    )

