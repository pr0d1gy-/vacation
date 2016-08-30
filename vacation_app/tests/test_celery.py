from datetime import datetime, timedelta
from random import randrange

from django.test import TestCase
from django.core import mail

from vacation_app.models.vacation import Vacation
from vacation_app.models.delivery import Delivery
from vacation_app.tests.utils import Utils
from vacation_app.tasks import notification_create_vacations,\
    notification_update_vacations, clear_old_rejected_vacations

from _vacation_project.settings import VACATION_REJECTED_DAYS_TO_REMOVE


class TestCeleryTasks(Utils, TestCase):

    def create_vacation(self, user=None):
        v = Vacation()
        v.date_start = self.get_date()
        v.date_end = self.get_date(bigger=1)

        if not user:
            v.user = self.user
        else:
            v.user = user

        v.save()

        return v

    def create_delivery(self, user=False, manager=False, admin=False):
        d = Delivery()
        d.address = 'test%s@test.test' % randrange(1, 1000)
        d.name = 'Test'
        d.action_user = user
        d.action_manager = manager
        d.action_admin = admin
        d.save()

        return d

    def test_clear_old_rejected_vacations(self):
        v1 = self.create_vacation()
        v2 = self.create_vacation(user=self.other_user)

        self.assertTrue(Vacation.objects.all().count() == 2)
        clear_old_rejected_vacations()
        self.assertTrue(Vacation.objects.all().count() == 2)

        Vacation.objects.filter(pk=v1.pk).update(
            state=Vacation.VACATION_REJECTED_BY_ADMIN,
            updated_at=(datetime.now() -
                        timedelta(days=VACATION_REJECTED_DAYS_TO_REMOVE + 1))
        )

        clear_old_rejected_vacations()
        self.assertTrue(Vacation.objects.all().count() == 1)

    def test_notification_create_vacations(self):
        v = self.create_vacation()
        notification_create_vacations(v.pk)
        self.assertTrue(len(mail.outbox) == 1)

        mail.outbox = []
        d = self.create_delivery(user=True)
        notification_create_vacations(v.pk)
        self.assertTrue(len(mail.outbox) == 2)

    def test_notification_update_vacations(self):
        v = self.create_vacation()
        d = self.create_delivery(user=True)
        d = self.create_delivery(manager=True)
        d = self.create_delivery(admin=True)

        d = self.create_delivery(manager=True, admin=True)

        v.state = Vacation.VACATION_APPROVED_BY_MANAGER
        v.save()

        notification_update_vacations(v.pk)

        self.assertTrue(len(mail.outbox) == 1)
        self.assertTrue(len(mail.outbox[0].to) == 2)

        mail.outbox = []
        v.state = Vacation.VACATION_REJECTED_BY_MANAGER
        v.save()

        notification_update_vacations(v.pk)
        self.assertTrue(len(mail.outbox) == 1)
        self.assertTrue(len(mail.outbox[0].to) == 2)

        mail.outbox = []
        v.state = Vacation.VACATION_REJECTED_BY_ADMIN
        v.save()

        notification_update_vacations(v.pk)
        self.assertTrue(len(mail.outbox) == 2)
        self.assertTrue(len(mail.outbox[1].to) == 2)

        mail.outbox = []
        v.state = Vacation.VACATION_APPROVED_BY_ADMIN
        v.save()

        notification_update_vacations(v.pk)
        self.assertTrue(len(mail.outbox) == 2)
        self.assertTrue(len(mail.outbox[1].to) == 2)
