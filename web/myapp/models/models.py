from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import gettext_lazy as _

from web.myapp.models.abstract import AbsctractModel


# Create your models here.
class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('U', _('Undefined')),
        ('M', _('Male')),
        ('F', _('Female'))
    )

    user = models.OneToOneField(User, unique=True)
    gender = models.CharField(choices=GENDER_CHOICES)


class Address(AbsctractModel):
    user = models.ForeignKey(User, related_name=_('addresses'))
    country = models.CharField()
    state = models.CharField()
    city = models.CharField()
    postcode = models.CharField()
    lat = models.FloatField()
    lon = models.FloatField()


class UserGroups(AbsctractModel):
    GROUP_CHOICES = (
        ('L1', _('Level 1')),
        ('L2', _('Level 2')),
        ('L3', _('Level 3')),
        ('L4', _('Level 4')),
        ('L5', _('Level 5')),
    )

    name = models.CharField(choices=GROUP_CHOICES)
    description = models.TextField()
