import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from TestDjango.settings import MEDIA_ROOT


class User(AbstractUser):
    country = models.CharField(_('country'), max_length=50, blank=True)
    city = models.CharField(_('city'), max_length=50, blank=True)
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='avatar')
