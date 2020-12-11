from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class User(AbstractUser):
    profile_name = models.CharField(_('Profile name'), max_length=40, null=True, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='user/avatars', blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True, db_index=True)

