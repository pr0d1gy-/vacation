from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, UserManager
from django.core import validators
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _

from vacation_app import tasks

class Employee(AbstractUser):
    GUSER = 1
    GMGER = 2
    GADMIN = 3
    GROUPS = (
        (GUSER, 'User'),
        (GMGER, 'Manager'),
        (GADMIN, 'Admin')
    )
    group_code = models.PositiveSmallIntegerField(choices=GROUPS, default=1)
    rang = models.CharField(max_length = 20)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return str(self.id) + ' ' + self.username


class Vacation(models.Model):
    VACATION_NEW = 1
    VACATION_APPROVED_BY_MANAGER = 20
    VACATION_REJECTED_BY_MANAGER = 21
    VACATION_APPROVED_BY_ADMIN = 30
    VACATION_REJECTED_BY_ADMIN = 31
    VACATIONS_STATES = (
        (VACATION_NEW, 'New'),
        (VACATION_APPROVED_BY_MANAGER, 'Approved by manager'),
        (VACATION_REJECTED_BY_MANAGER, 'Rejected by manager'),
        (VACATION_APPROVED_BY_ADMIN, 'Approved by admin'),
        (VACATION_REJECTED_BY_ADMIN, 'Rejected by admin')
    )
    user = models.ForeignKey(Employee)
    date_start = models.DateField()
    date_end = models.DateField()
    comment_user = models.TextField(blank=True, null=True)
    comment_admin = models.TextField(blank=True, null=True)
    state = models.SmallIntegerField(choices=VACATIONS_STATES, default=1)

    def __str__(self):
        return str(self.id) + ' ' + self.date_start.strftime("%Y-%m-%d") + '||' + self.date_end.strftime("%Y-%m-%d")+ ' ' + self.user.username

    def clean(self):
        if self.date_start > self.date_end:
            raise ValidationError({'date_start': 'Date start bigger date end'})


class Delivery(models.Model):
    address = models.EmailField(max_length=20)
    name = models.CharField(max_length=20)
    state = models.BooleanField(default=True)
    action_user = models.BooleanField(default=True)
    action_manager = models.BooleanField(default=True)
    action_admin = models.BooleanField(default=True)

    def __str__(self):
        return self.address


def send_mails(instance, created, **kwargs):
    groups = {}
    for item in Employee.GROUPS:
        groups.update({item[0]: item[1]})
    print groups
    if created:
        group_code = instance.user.group_code
        subject = 'vacation create by '
        message = instance.user.username + ' created new vacation' + ' '\
                  + instance.date_start.strftime("%Y-%m-%d") + ' - ' + instance.date_end.strftime("%Y-%m-%d")
    else:
        subject = 'vacation update by '
        if instance.state in [Vacation.VACATION_APPROVED_BY_MANAGER, Vacation.VACATION_REJECTED_BY_MANAGER]:
            group_code = Employee.GMGER
        elif instance.state in [Vacation.VACATION_APPROVED_BY_ADMIN, Vacation.VACATION_REJECTED_BY_ADMIN]:
            group_code = Employee.GADMIN
        message = instance.user.username + ' wants on vacation ' + instance.date_start.strftime("%Y-%m-%d") \
                  + ' - ' + instance.date_end.strftime("%Y-%m-%d")

    subject += groups[group_code]
    print subject
    print message
    # tasks.delivery_send.delay(subject=subject, message=message)
    tasks.delivery_send(subject=subject, message=message, group_code=group_code)



post_save.connect(send_mails, sender=Vacation)
