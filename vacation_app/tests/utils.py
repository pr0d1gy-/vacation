from datetime import datetime, timedelta

from django.db.models import signals

from vacation_app.models.employee import Employee
from vacation_app.models.vacation import Vacation
from vacation_app.signals.vacation import vacation_post_save

from rest_framework.authtoken.models import Token


class Utils(object):

    now = None

    user = None
    user_token = None
    other_user = None
    other_user_token = None
    mger = None
    mger_token = None
    admin = None
    admin_token = None

    def setUp(self):
        self.user = Employee.objects.create(
            username='user',
            email='user@host.ua',
            rang='develop',
            group_code=Employee.GUSER
        )
        self.user.set_password('12345')
        self.user.save()
        self.user_token = Token.objects.create(user=self.user)

        self.other_user = Employee.objects.create(
            username='other_user',
            email='other_user@host.ua',
            rang='develop',
            group_code=Employee.GUSER
        )
        self.other_user.set_password('12345')
        self.other_user.save()
        self.other_user_token = Token.objects.create(user=self.other_user)

        self.mger = Employee.objects.create(
            username='manager',
            email='manager@host.ua',
            rang='manager',
            group_code=Employee.GMGER
        )
        self.mger.set_password('12345')
        self.mger.save()
        self.mger_token = Token.objects.create(user=self.mger)

        self.admin = Employee.objects.create(
            username='admin',
            password='12345',
            email='admin@host.ua',
            rang='administrator',
            group_code=Employee.GADMIN
        )
        self.admin.set_password('12345')
        self.admin.save()
        self.admin_token = Token.objects.create(user=self.admin)

        self.now = datetime.now()

        signals.post_save.disconnect(
            receiver=vacation_post_save,
            sender=Vacation,
            weak=True,
            dispatch_uid='vacation_post_save'
        )

    def get_date(self, d=None, bigger=0):
        return (d if d else self.now).date() if not bigger else \
            ((d if d else self.now) + timedelta(days=bigger)).date()
