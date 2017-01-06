from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import gettext_lazy as _

from .abstract import AbsctractModel


# Create your models here.
# class AssessorGroups(Group):
#     GROUP_CHOICES = (
#         ('L1', _('Level 1')),
#         ('L2', _('Level 2')),
#         ('L3', _('Level 3')),
#         ('L4', _('Level 4')),
#         ('L5', _('Level 5')),
#     )
#
#     name = models.CharField(_('name'), max_length=80, unique=True,
#                             choices=GROUP_CHOICES)
#     description = models.TextField()
#
#
class AssessorModel(User):
    parent = models.ForeignKey(ContentType, related_name=_('assessors'),
                               related_query_name=_('assessor'))
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('parent', 'object_id')


class AssessorProfile(models.Model):
    GENDER_CHOICES = (
        ('U', _('Undefined')),
        ('M', _('Male')),
        ('F', _('Female'))
    )

    user = models.OneToOneField(AssessorModel, unique=True,
                                on_delete=models.CASCADE,
                                related_name=_('profile'))
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    picture = models.FileField(blank=True)


class Address(AbsctractModel):
    user = models.ForeignKey(AssessorModel, related_name=_('addresses'),
                             related_query_name=_('address'),
                             on_delete=models.CASCADE)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    postcode = models.CharField(max_length=30)
    lat = models.FloatField()
    lon = models.FloatField()
