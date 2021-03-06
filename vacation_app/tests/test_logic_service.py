from django.test import TestCase

from vacation_app.models.employee import Employee
from vacation_app.models.vacation import Vacation
from vacation_app.services import VacationService, ServiceException
from vacation_app.tests.utils import Utils


class TestLogicService(Utils, TestCase):

    def test_logic_add_vacation_user(self):
        user = Employee.objects.all().first()

        vacation = VacationService(user=user).add_vacation(
            date_start=self.get_date(),
            date_end=self.get_date(bigger=1),
            comment_user='comment'
        )

        self.assertIsInstance(vacation, Vacation)
        self.assertEqual(Vacation.objects.count(), 1)

    def test_logic_add_vacation_unknown(self):
        self.assertRaises(
            ServiceException,
            lambda: VacationService().add_vacation(
                date_start=self.get_date(),
                date_end=self.get_date(bigger=1),
                comment_user='comment'
            )
        )

        self.assertEqual(Vacation.objects.count(), 0)

    def test_logic_add_vacation_date_start_bigger_date_end(self):
        user = Employee.objects.all().first()

        self.assertRaises(
            ServiceException,
            lambda: VacationService(user=user).add_vacation(
                date_start=self.get_date(bigger=1),
                date_end=self.get_date(),
                comment_user='comment'
            )
        )

    def test_logic_add_vacation_delta_dates_bigger_14(self):
        user = Employee.objects.all().first()

        self.assertRaises(
            ServiceException,
            lambda: VacationService(user=user).add_vacation(
                date_start=self.get_date(),
                date_end=self.get_date(bigger=15),
                comment_user='comment'
            )
        )

        self.assertEqual(Vacation.objects.count(), 0)

    def test_logic_add_vacation_summary_date_bigger_14(self):
        user = Employee.objects.all().first()

        vacation = VacationService(user=user).add_vacation(
            date_start=self.get_date(),
            date_end=self.get_date(bigger=14),
            comment_user='comment'
        )

        self.assertIsInstance(vacation, Vacation)
        self.assertEqual(Vacation.objects.count(), 1)

        self.assertRaises(
            ServiceException,
            lambda: VacationService(user=user).add_vacation(
                date_start=self.get_date(),
                date_end=self.get_date(bigger=3),
                comment_user='comment'
            )
        )

        self.assertEqual(Vacation.objects.count(), 1)

    def test_logic_add_vacation_summary_date_bigger_14_2_year(self):
        user = Employee.objects.all().first()

        vacation = VacationService(user=user).add_vacation(
            date_start=self.get_date(),
            date_end=self.get_date(bigger=14),
            comment_user='comment'
        )

        self.assertIsInstance(vacation, Vacation)
        self.assertEqual(Vacation.objects.count(), 1)

        vacation = VacationService(user=user).add_vacation(
            date_start=self.get_date(bigger=365),
            date_end=self.get_date(bigger=(14 + 365)),
            comment_user='comment'
        )

        self.assertIsInstance(vacation, Vacation)
        self.assertEqual(Vacation.objects.count(), 2)

    def test_logic_add_vacation_bad_data(self):
        user = Employee.objects.all().first()

        self.assertRaises(
            ServiceException,
            lambda: VacationService(user=user).add_vacation(
                date_start=45,
                date_end=self.get_date(),
                comment_user='comment'
            )
        )

        self.assertRaises(
            ServiceException,
            lambda: VacationService(user=user).add_vacation(
                date_start=self.get_date(),
                date_end=45,
                comment_user='comment'
            )
        )

        self.assertEqual(Vacation.objects.count(), 0)

    def test_logic_update_vacation_by_user(self):
        user = Employee.objects.filter(group_code=Employee.GUSER).first()

        vacation = VacationService(user=user).add_vacation(
            date_start=self.get_date(),
            date_end=self.get_date(bigger=14),
            comment_user='comment'
        )

        self.assertIsInstance(vacation, Vacation)
        self.assertEqual(Vacation.objects.count(), 1)

        self.assertRaises(
            ServiceException,
            lambda: VacationService(user=user).update_vacation(
                vacation=vacation,
                state=Vacation.VACATION_APPROVED_BY_MANAGER
            )
        )

        self.assertRaises(
            ServiceException,
            lambda: VacationService(user=user).update_vacation(
                vacation=vacation,
                state=Vacation.VACATION_APPROVED_BY_ADMIN
            )
        )

    def test_logic_update_vacation_by_manager(self):
        user = Employee.objects.filter(group_code=Employee.GUSER).first()
        manager = Employee.objects.filter(group_code=Employee.GMGER).first()

        vacation = VacationService(user=user).add_vacation(
            date_start=self.get_date(),
            date_end=self.get_date(bigger=14),
            comment_user='comment'
        )

        self.assertIsInstance(vacation, Vacation)
        self.assertEqual(Vacation.objects.count(), 1)

        VacationService(user=manager).update_vacation(
            vacation=vacation,
            state=Vacation.VACATION_APPROVED_BY_MANAGER
        )

        self.assertEqual(Vacation.objects.get(pk=vacation.id).state,
                         Vacation.VACATION_APPROVED_BY_MANAGER)

        self.assertRaises(
            ServiceException,
            lambda: VacationService(user=manager).update_vacation(
                vacation=vacation,
                state=Vacation.VACATION_APPROVED_BY_ADMIN
            )
        )

    def test_logic_update_vacation_by_admin(self):
        user = Employee.objects.filter(group_code=Employee.GUSER).first()
        admin = Employee.objects.filter(group_code=Employee.GADMIN).first()

        vacation = VacationService(user=user).add_vacation(
            date_start=self.get_date(),
            date_end=self.get_date(bigger=14),
            comment_user='comment'
        )

        self.assertIsInstance(vacation, Vacation)
        self.assertEqual(Vacation.objects.count(), 1)

        VacationService(user=admin).update_vacation(
            vacation=vacation,
            state=Vacation.VACATION_REJECTED_BY_ADMIN
        )

        self.assertEqual(Vacation.objects.get(pk=vacation.id).state,
                         Vacation.VACATION_REJECTED_BY_ADMIN)
