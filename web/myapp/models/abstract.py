# -*- coding: utf-8 -*-
"""
 * Project: political-advisor
 * Author name: Iraquitan Cordeiro Filho
 * Author email: iraquitanfilho@gmail.com
 * Author login: pma007
 * File: abstract
 * Date: 12/14/16
 * Time: 15:09
 * Description: Add script info here.
.. moduleauthor:: Iraquitan Cordeiro Filho <iraquitanfilho@gmail.com>

"""
import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbsctractModel(models.Model):

    class Meta:
        abstract = True

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(verbose_name=_('Created'),
                                        auto_now_add=True)
    date_modified = models.DateTimeField(verbose_name=_('Last modified'),
                                         auto_now=True)
