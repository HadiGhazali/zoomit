from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_password(password):
    if len(password) < 8:
        raise ValidationError(_('password is too short'), code='invalid')


def validate_username(username):
    try:
        User.objects.get(username=username)
        raise ValidationError(
            _('this user name is already exist'),
            code='invalid'
        )
    except User.DoesNotExist:
        return username

