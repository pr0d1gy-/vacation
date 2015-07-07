from django.db import models
from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    GUSER = 1
    GMGER = 2
    GADMIN = 3

    GROUPS = (
        (GUSER, 'User'),
        (GMGER, 'Manager'),
        (GADMIN, 'Admin')
    )

    group_code = models.PositiveSmallIntegerField(choices=GROUPS, default=GUSER)
    rang = models.CharField(max_length=20)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return str(self.id) + ' ' + self.username
