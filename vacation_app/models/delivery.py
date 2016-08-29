from django.db import models
from django.utils.translation import ugettext_lazy as _


class Delivery(models.Model):

    address = models.EmailField(
        max_length=20, unique=True, verbose_name=_('Address'))
    name = models.CharField(
        max_length=20, verbose_name=_('Name'))
    state = models.BooleanField(
        default=True, db_index=True, verbose_name=_('State'))
    action_user = models.BooleanField(
        default=True, db_index=True, verbose_name=_('Action user'))
    action_manager = models.BooleanField(
        default=True, db_index=True, verbose_name=_('Action manager'))
    action_admin = models.BooleanField(
        default=True, db_index=True, verbose_name=_('Action admin'))

    def __str__(self):
        return self.address
