from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # search the UserModel database for an existing user with corresponding email (or username for superuser)
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist: # I'm not 100% sure what this does..., but the authentication will fail
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned: # if theres multiple users with the same email, return the one with lowest id (should never happen??)
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()
        
        # check password and is_active attribute of the user (currently unsued in our custom user)
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

