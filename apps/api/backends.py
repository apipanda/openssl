from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.validators import validate_email


class AuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        # If username is an email address, then try to pull it up
        try:
            validate_email(username)
            is_email = True
        except ValueError:
            is_email = False

        if is_email:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            # We have a non-email address username we should try username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user
