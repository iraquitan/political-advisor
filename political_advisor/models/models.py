from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .abstract import AbstractModel


# Create your models here.
# class CustomModelBackend(ModelBackend):
#     """
#     Authenticates against settings.AUTH_USER_MODEL.
#     """
#
#     def authenticate(self, email=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         if email is None:
#             email = kwargs.get(UserModel.USERNAME_FIELD)
#         try:
#             user = UserModel._default_manager.get_by_natural_key(email)
#         except UserModel.DoesNotExist:
#             # Run the default password hasher once to reduce the timing
#            # difference between an existing and a non-existing user (#20760).
#             UserModel().set_password(password)
#         else:
#             if user.check_password(password) and self.user_can_authenticate(
#                     user):
#                 return user
#
#
# class CustomUserManager(BaseUserManager):
#     use_in_migrations = True
#
#     def _create_user(self, email, password, **extra_fields):
#         """
#         Creates and saves a User with the given email and password.
#         """
#         if not email:
#             raise ValueError('The given email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         return self._create_user(email, password, **extra_fields)
#
#
# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     """
#     An abstract base class implementing a fully featured User model with
#     admin-compliant permissions.
#
#     Email and password are required. Other fields are optional.
#     """
#     USER_CHOICES = (
#         (_('SU'), _('Super User')),
#         (_('AU'), _('Assessor User'))
#     )
#
#     email = models.EmailField(_('email address'), unique=True)
#     first_name = models.CharField(_('first name'), max_length=30, blank=True)
#     last_name = models.CharField(_('last name'), max_length=30, blank=True)
#     is_active = models.BooleanField(
#         _('active'),
#         default=True,
#         help_text=_(
#             'Designates whether this user should be treated as active. '
#             'Unselect this instead of deleting accounts.'
#         ),
#     )
#    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
#
#     user_type = models.CharField(max_length=2, choices=USER_CHOICES,
#                                  default='SU')
#     parent = models.ForeignKey(settings.AUTH_USER_MODEL,
#                                on_delete=models.CASCADE,
#                                related_name=_('user_parent'), blank=True,
#                                null=True)
#     super_user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                                    on_delete=models.CASCADE,
#                                    related_name=_('user_super_user'),
#                                    blank=True, null=True)
#
#     objects = CustomUserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')
#         unique_together = ('email', 'user_type')
#
#     def get_full_name(self):
#         """
#         Returns the first_name plus the last_name, with a space in between.
#         """
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()
#
#     def get_short_name(self):
#         """
#         Returns the short name for the user.
#         """
#         return self.first_name
#
#     def email_user(self, subject, message, from_email=None, **kwargs):
#         """
#         Sends an email to this User.
#         """
#         send_mail(subject, message, from_email, [self.email], **kwargs)


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
