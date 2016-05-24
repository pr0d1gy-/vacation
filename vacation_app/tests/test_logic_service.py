import datetime

from django.test import TestCase

from vacation_app.models.employee import Employee
from vacation_app.models.vacation import Vacation

from vacation_app.services import VacationService, ServiceException


class TestLogicService(TestCase):

    def setUp(self):
        user = Employee.objects.create(
            username='user',
            email='user@host.ua',
            rang='develop',
            group_code=Employee.GUSER
        )
        user.set_password('12345')
        user.save()
        mger = Employee.objects.create(
            username='manager',
            email='manager@host.ua',
            rang='manager',
            group_code=Employee.GMGER
        )
        mger.set_password('12345')
        mger.save()
        admin = Employee.objects.create(
            username='admin',
            password='12345',
            email='admin@host.ua',
            rang='administrator',
            group_code=Employee.GADMIN
        )
        admin.set_password('12345')
        admin.save()

    def test_logic_add_vacation_user(self):
        user = Employee.objects.all().first()
        vacation = VacationService(user=user).add_vacation(
            date_start=datetime.datetime.strptime('2015-08-08', "%Y-%m-%d").date(),
            date_end=datetime.datetime.strptime('2015-08-09', "%Y-%m-%d").date(),
            comment_user='comment'
        )
        self.assertEqual(len(Vacation.objects.all()), 1)

    def test_logic_add_vacation_unknown(self):
        VacationService().add_vacation(
            date_start=datetime.datetime.strptime('2015-08-08', "%Y-%m-%d").date(),
            date_end=datetime.datetime.strptime('2015-08-09', "%Y-%m-%d").date(),
            comment_user='comment'
        )
        self.assertEqual(len(Vacation.objects.all()), 0)

    def test_logic_add_vacation_date_start_bigger_date_end(self):
        user = Employee.objects.all().first()
        vacation = VacationService(user=user).add_vacation(
            date_start=datetime.datetime.strptime('2015-08-10', "%Y-%m-%d").date(),
            date_end=datetime.datetime.strptime('2015-08-09', "%Y-%m-%d").date(),
            comment_user='comment'
        )
        self.assertRaises(ServiceException, lambda: Vacation.add_vacation())

    def test_logic_add_vacation_delta_dates_bigger_14(self):
        user = Employee.objects.all().first()
        print VacationService(user=user).add_vacation(
            date_start=datetime.datetime.strptime('2015-08-10', "%Y-%m-%d").date(),
            date_end=datetime.datetime.strptime('2015-08-25', "%Y-%m-%d").date(),
            comment_user='comment'
        )
        # self.assertEqual(len(Vacation.objects.all()), 0)
        self.assertRaises(ServiceException())

    def test_logic_add_vacation_summary_date_bigger_14(self):
        user = Employee.objects.all().first()
        vacation = VacationService(user=user).add_vacation(
            date_start=datetime.datetime.strptime('2015-08-10', "%Y-%m-%d").date(),
            date_end=datetime.datetime.strptime('2015-08-24', "%Y-%m-%d").date(),
            comment_user='comment'
        )
        self.assertEqual(len(Vacation.objects.all()), 1)
        vacation = VacationService(user=user).add_vacation(
            date_start=datetime.datetime.strptime('2015-08-10', "%Y-%m-%d").date(),
            date_end=datetime.datetime.strptime('2015-08-24', "%Y-%m-%d").date(),
            comment_user='comment'
        )
        self.assertEqual(len(Vacation.objects.all()), 1)

    def test_logic_add_vacation_summary_date_bigger_14_2_year(self):
        user = Employee.objects.all().first()
        vacation = VacationService(user=user).add_vacation(
            date_start=datetime.datetime.strptime('2015-08-10', "%Y-%m-%d").date(),
            date_end=datetime.datetime.strptime('2015-08-24', "%Y-%m-%d").date(),
            comment_user='comment'
        )
        self.assertEqual(len(Vacation.objects.all()), 1)
        vacation = VacationService(user=user).add_vacation(
            date_start=datetime.datetime.strptime('2016-08-10', "%Y-%m-%d").date(),
            date_end=datetime.datetime.strptime('2016-08-24', "%Y-%m-%d").date(),
            comment_user='comment'
        )
        self.assertEqual(len(Vacation.objects.all()), 2)

    def test_logic_add_vacation_bad_data(self):
        user = Employee.objects.all().first()
        vacation = VacationService(user=user).add_vacation(
            date_start=45,
            date_end=datetime.datetime.strptime('2015-08-24', "%Y-%m-%d").date(),
            comment_user='comment'
        )

    def test_logic_update_vacation_by_user(self):
        user = Employee.objects.all().filter(group_code=Employee.GUSER).first()
        VacationService(user=user).add_vacation(
            date_start=datetime.datetime.strptime('2015-08-10', "%Y-%m-%d").date(),
            date_end=datetime.datetime.strptime('2015-08-24', "%Y-%m-%d").date(),
            comment_user='comment'
        )
        manager = Employee.objects.all().filter(group_code=Employee.GUSER).first()
        vacation = Vacation.objects.get(user=user)
        for state in Vacation.VACATIONS_STATES:

            VacationService(user=manager).update_vacation(
                vacation=vacation,
                state=state[0],
                # comment_admin='man'
            )
            if vacation.state in [Vacation.VACATION_APPROVED_BY_MANAGER,
                            Vacation.VACATION_REJECTED_BY_MANAGER]:
                continue
            if state[0] in [Vacation.VACATION_APPROVED_BY_MANAGER,
                            Vacation.VACATION_REJECTED_BY_MANAGER]:
                self.assertEqual(Vacation.objects.get(user=user).state, state[0])
