from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .validators import schoolEmailValidator, bikeSizeValidator
from django.urls import reverse

# refer to ERM diagrams on my tablet
# some comments refer to features which haven't been implemented yet!!


# the custom user doesn't have a username field, but uses the email as unique identifier
class User(AbstractUser):
    
    # change label of first_name to preferred name
    first_name = models.CharField(_("preferred name"), max_length=150, blank=True)


    email = models.EmailField(
        # set a "verbose name" (not sure what is does...). I think it displays this name when rendered as html
        _('email address'), 
        # set email field as unique, necessary to be used for authentication
        unique=True, 
        # add validator to check for a valid school email
        validators=[schoolEmailValidator], 
        # custom error message
        error_messages={
            "unique": _("A user with that email already exists.")
        }
    )

    # if printed, return only the preferred name
    def __str__(self) -> str:        
        return self.first_name
    
        
    def get_absolute_url(self):
        return reverse('user-change', kwargs={'pk': self.pk})
    

class Bike(models.Model):
    
    SIZES = [
        # (string stored in database, human readable description)
        ("", "Select bike size."),
        ("S", "small"),
        ("M", "medium"),
        ("L", "large"),
    ]
    
    number = models.IntegerField(
        # set as unique to distinguish different bikes
        unique=True, 
        help_text="Number as it appears on the bike locks/keys"
    )

    size = models.CharField(
        # either small (s), medium (m) or large (l)
        max_length=1, 
        # constrain possible values to SIZES
        choices=SIZES,
        default="",
        validators=[bikeSizeValidator],
    )

    steward = models.ForeignKey(
        # a user who is the current bike steward
        User, 
        # if the referenced user is manually deleted, prevent the deletion until a new bike steward is set for this bike
        on_delete=models.PROTECT
    )

    def __str__(self) -> str:
        return str(self.number)


class Issue(models.Model):
    # max length around 50 words
    title = models.CharField(max_length=250) 
    # max length around 300 words
    description = models.CharField(max_length=1500) 
    time_raised = models.DateTimeField()
    time_resolved = models.DateTimeField()
    is_resolved = models.BooleanField()


class Borrowing(models.Model):
    # the anticipated start and end times of the borrowing
    start_time = models.DateTimeField(help_text="Leave blank for current time")
    # end time needn't be defined when starting a borrowing, but it can be set to an anticipated time to indicate when a bike might become available in the future?? 
    # if endtime is unset, it is assumed that the bike is being borrowed indefinetly (until it is acutally returned)
    end_time = models.DateTimeField()

    borrower = models.ForeignKey(
        # which user borrowed the bike
        User,
        # If the user is deleted, the associated borrowings are deleted too
        on_delete=models.CASCADE,
    )
    
    borrowed_bike = models.ForeignKey(
        # which bike borrowed was borrowed
        Bike,
        # If the bike is deleted, the associated borrowings are deleted too
        on_delete=models.CASCADE
    )

    # if the key has been successfully given out/returned to the student
    key_received = models.BooleanField()
    key_returned = models.BooleanField()

    issue = models.ForeignKey(
        # if something requires manual attention, the borrower can attach an issue to the borrowing which will notify the bike steward for them to resolve it
        Issue, 
        # prevent the corresponding issue to be deleted (to keep a record)
        on_delete=models.PROTECT
        )

    # returns a short readable string with all information
    def __str__(self) -> str:
        return "{0} borrowed {1} at {2}".format(
            self.borrower,
            self.borrowed_bike,
            self.start_time,
        )

    




