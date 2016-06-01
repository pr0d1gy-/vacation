from datetime import datetime, timedelta

from vacation_app.models.employee import Employee


class Utils(object):

    now = None

    user = None
    mger = None
    admin = None

    def setUp(self):
        self.user = Employee.objects.create(
            username='user',
            email='user@host.ua',
            rang='develop',
            group_code=Employee.GUSER
        )
        self.user.set_password('12345')
        self.user.save()

        self.mger = Employee.objects.create(
            username='manager',
            email='manager@host.ua',
            rang='manager',
            group_code=Employee.GMGER
        )
        self.mger.set_password('12345')
        self.mger.save()

        self.admin = Employee.objects.create(
            username='admin',
            password='12345',
            email='admin@host.ua',
            rang='administrator',
            group_code=Employee.GADMIN
        )
        self.admin.set_password('12345')
        self.admin.save()

        self.now = datetime.now()

    def get_date(self, d=None, bigger=0):
        return (d if d else self.now).date() if not bigger else \
            ((d if d else self.now) + timedelta(days=bigger)).date()
