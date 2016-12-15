from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import gettext_lazy as _

from web.myapp.models.abstract import AbsctractModel


# Create your models here.
class AssessorModel(User):
    parent = models.ForeignKey(User, related_name=_('assessors'),
                               related_query_name=_('assessor'))
    groups = models.ManyToManyField(
        AssessorGroups,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )


class AssessorProfile(models.Model):
    GENDER_CHOICES = (
        ('U', _('Undefined')),
        ('M', _('Male')),
        ('F', _('Female'))
    )

    user = models.OneToOneField(AssessorModel, unique=True)
    gender = models.CharField(choices=GENDER_CHOICES)
    picture = models.FilePathField()


class AssessorAddress(AbsctractModel):
    user = models.ForeignKey(AssessorModel, related_name=_('addresses'),
                             related_query_name=_('address'))
    country = models.CharField()
    state = models.CharField()
    city = models.CharField()
    postcode = models.CharField()
    lat = models.FloatField()
    lon = models.FloatField()


class AssessorGroups(Group):
    GROUP_CHOICES = (
        ('L1', _('Level 1')),
        ('L2', _('Level 2')),
        ('L3', _('Level 3')),
        ('L4', _('Level 4')),
        ('L5', _('Level 5')),
    )

    name = models.CharField(_('name'), max_length=80, unique=True,
                            choices=GROUP_CHOICES)
    description = models.TextField()
