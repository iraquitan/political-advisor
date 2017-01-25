from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .abstract import AbstractModel


# Create your models here.
class EmailBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL using email.
    """

    def authenticate(self, username=None, password=None, user_type=None,
                     **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username, user_type=user_type)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(
                    user):
                return user
        return None


class CustomUser(AbstractUser):
    USER_CHOICES = (
        (_('SU'), _('Super User')),
        (_('AU'), _('Assessor User'))
    )
    user_type = models.CharField(max_length=2, choices=USER_CHOICES,
                                 default='SU')
    parent = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name=_('user_parent'), blank=True,
                               null=True)
    super_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name=_('user_super_user'),
                                   blank=True, null=True)

    class Meta:
        unique_together = ('email', 'user_type')


class Profile(models.Model):
    GENDER_CHOICES = (
        ('U', _('Undefined')),
        ('M', _('Male')),
        ('F', _('Female'))
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=2)
    picture = models.FileField(blank=True, null=True)


class Address(AbstractModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name=_('addresses'),
                             related_query_name=_('address'),
                             on_delete=models.CASCADE)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    postcode = models.CharField(max_length=30)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
