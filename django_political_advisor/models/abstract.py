import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractModel(models.Model):

    class Meta:
        abstract = True

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(verbose_name=_('Created'),
                                        auto_now_add=True)
    date_modified = models.DateTimeField(verbose_name=_('Last modified'),
                                         auto_now=True)
