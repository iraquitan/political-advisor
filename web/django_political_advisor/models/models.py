from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .abstract import AbstractModel


# Create your models here.
class AssessorModel(User):
    content_type = models.ForeignKey(ContentType, related_name=_('assessors'),
                                     related_query_name=_('assessor'),
                                     verbose_name='parent',
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


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
    picture = models.FileField(blank=True, null=True)


class Address(AbstractModel):
    user = models.ForeignKey(AssessorModel, related_name=_('addresses'),
                             related_query_name=_('address'),
                             on_delete=models.CASCADE)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    postcode = models.CharField(max_length=30)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
