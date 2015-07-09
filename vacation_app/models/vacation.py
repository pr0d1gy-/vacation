from django.core.exceptions import ValidationError
from django.db import models
from vacation_app.models.employee import Employee


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
        return \
            str(self.id) + ' ' + \
            self.date_start.strftime("%Y-%m-%d") + '||' + \
            self.date_end.strftime("%Y-%m-%d") + ' ' + \
            self.user.username

    def clean(self):
        if self.date_start > self.date_end:
            raise ValidationError({
                'date_start': 'Date start bigger date end'
            })
