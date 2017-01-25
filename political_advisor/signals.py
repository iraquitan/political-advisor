from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from political_advisor.utils import get_unique_username
from .models.models import Profile, CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_save, sender=CustomUser)
def create_username(sender, instance, **kwargs):
    if not instance.id:
        username = get_unique_username(instance)
        instance.username = username
