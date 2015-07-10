import datetime

from django.core.exceptions import ValidationError
from django.db import models

from vacation_app.models.employee import Employee


class Vacation(models.Model):

    # Maximum days of vacations
    VACATION_DAY_LIMIT = 14

    # Vacation status
    VACATION_NEW = 1
    VACATION_APPROVED_BY_MANAGER = 20
    VACATION_REJECTED_BY_MANAGER = 21
    VACATION_APPROVED_BY_ADMIN = 30
    VACATION_REJECTED_BY_ADMIN = 31

    # Vacation status choices
    VACATIONS_STATES = (
        (VACATION_NEW, 'New'),
        (VACATION_APPROVED_BY_MANAGER, 'Approved by manager'),
        (VACATION_REJECTED_BY_MANAGER, 'Rejected by manager'),
        (VACATION_APPROVED_BY_ADMIN, 'Approved by admin'),
        (VACATION_REJECTED_BY_ADMIN, 'Rejected by admin')
    )

    # Vacation Fields
    user = models.ForeignKey(Employee)
    date_start = models.DateField(db_index=True)
    date_end = models.DateField(db_index=True)
    comment_user = models.TextField(blank=True, null=True)
    comment_admin = models.TextField(blank=True, null=True)
    state = models.SmallIntegerField(choices=VACATIONS_STATES, default=1,
                                     db_index=True)

    def __str__(self):
        return str(self.id) + ' ' + \
            self.date_start.strftime("%Y-%m-%d") + '||' + \
            self.date_end.strftime("%Y-%m-%d") + ' ' + \
            self.user.username

    def clean_date_start(self):
        if self.date_start > self.date_end:
            raise ValidationError({
                'date_start': 'Date start bigger than date end.'
            })

    def clean_date_end(self):
        days = self.get_vacation_days()

        if days > self.VACATION_DAY_LIMIT:
            raise ValidationError({
                'date_end': 'Quantity of Vacation days bigger than %s.' % (
                    self.VACATION_DAY_LIMIT
                )
            })

    def clean(self):
        self.clean_date_start()
        self.clean_date_end()

        vacation_days = self.get_vacation_days()

        if not vacation_days:
            raise ValidationError({
                'date_end': 'Selected vacations period is invalid.'
            })

        if not self.id:
            days = self.get_vacations_days_by_user()
            # Check used days
            if days >= self.VACATION_DAY_LIMIT:
                raise ValidationError({
                    'date_start': ('Creating an application is not available.'
                                   ' Days used %s of %s') % (
                        days,
                        self.VACATION_DAY_LIMIT
                    )
                })

            # Check available days
            available_days = self.VACATION_DAY_LIMIT - days
            if vacation_days > available_days:
                raise ValidationError({
                    'date_end': ('Selected period is larger than allowed. '
                                 'Possible to select %s of the days.') % (
                        available_days
                    )
                })

        return super(Vacation, self).clean()

    def get_vacation_days(self):
        return (self.date_end - self.date_start).days

    def get_vacations_days_by_user(self, user=None):
        # Get vacation for user
        queryset = Vacation.objects.filter(
            user=(self.user if not user else user)
        )

        # Exclude vacation for rejected status
        queryset = queryset.exclude(
            models.Q(state=self.VACATION_REJECTED_BY_ADMIN) |
            models.Q(state=self.VACATION_REJECTED_BY_MANAGER)
        )

        # Get vacations for current year
        queryset = queryset.filter(
            date_start__gte=datetime.date(self.date_start.year, 1, 1)
        )

        if not queryset:
            return 0

        # Calculate days
        days = 0
        for vacation in queryset:
            days += (vacation.date_end - vacation.date_start).days

        return days

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # Run clean methods
        self.full_clean()

        super(Vacation, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )
