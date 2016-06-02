from rest_framework import status


from rest_framework.test import APITestCase

from vacation_app.models.employee import Employee
from vacation_app.models.vacation import Vacation

from vacation_app.tests.api_url import APIUrl
from vacation_app.tests.api_user import ApiUser
from vacation_app.tests.utils import Utils


class APITests(Utils, ApiUser, APITestCase):

    login = ApiUser()

    user_vacation = None

    def setUp(self):
        super(APITests, self).setUp()

        self.user_vacation = Vacation.objects.create(
            user=self.user,
            date_start=self.get_date(),
            date_end=self.get_date(bigger=1),
            comment_user='comment_user',
            comment_admin='comment_admin',
            state=Vacation.VACATION_NEW
        )

        self.other_user_vacation = Vacation.objects.create(
            user=self.other_user,
            date_start=self.get_date(),
            date_end=self.get_date(bigger=1),
            comment_user='comment_user',
            comment_admin='comment_admin',
            state=Vacation.VACATION_NEW
        )

    def test_user_create(self):
        response = self.client.post(APIUrl.users, {
            'username': 'andrey',
            'password': '12345',
            'email': 'andr@exemple.com',
            'rang': 'some',
            'group_code': '2'
        })

        self.assertEqual(response.data['group_code'], Employee.GUSER)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_users_unknown_list(self):
        response = self.client.get(APIUrl.users)

        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_users_unknown_retrieve(self):
        users = Employee.objects.all()
        for user in users:
            response = self.client.get(APIUrl.users_id(user.id))

            self.assertEqual(response.status_code,
                             status.HTTP_401_UNAUTHORIZED)

    def test_users_unknown_delete(self):
        users = Employee.objects.all()
        for user in users:
            response = self.client.delete(APIUrl.users_id(user.id))

            self.assertEqual(response.status_code,
                             status.HTTP_401_UNAUTHORIZED)

    def test_users_unknown_update(self):
        users = Employee.objects.all()
        for user in users:
            response = self.client.put(APIUrl.users_id(user.id), {
                'username': 'andrey',
                'password': '12345',
                'email': 'andr@exemple.com',
                'rang': 'some',
                'group_code': '2'
            })

            self.assertEqual(response.status_code,
                             status.HTTP_401_UNAUTHORIZED)

    def test_users_user_list(self):
        self.login_user()
        response = self.client.get(APIUrl.users)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_users_user_retrieve_self(self):
        login_user = self.login_user()
        response = self.client.get(APIUrl.users_id(login_user.id))

        data = {key: login_user.__getattribute__(key)
                for key in response.data.keys()}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_users_user_retrieve_other(self):
        login_user = self.login_user()
        users = Employee.objects.all()
        for user in users:
            if user.id == login_user.id:
                continue

            response = self.client.get(APIUrl.users_id(user.id))

            self.assertEqual(response.status_code,
                             status.HTTP_404_NOT_FOUND)

    def test_users_user_delete(self):
        self.login_user()
        users = Employee.objects.all()
        for user in users:
            response = self.client.delete(APIUrl.users_id(user.id))

            self.assertEqual(response.status_code,
                             status.HTTP_404_NOT_FOUND)

    def test_users_user_update_self(self):
        login_user = self.login_user()
        response = self.client.put(APIUrl.users_id(login_user.id), {
            'username': 'andrey',
            'password': '12345',
            'email': 'andr@exemple.com',
            'rang': 'some',
            'group_code': '2'
        })

        self.assertEqual(response.data['group_code'], login_user.group_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_user_update_other(self):
        login_user = self.login_user()
        users = Employee.objects.all()
        for user in users:
            if user.id == login_user.id:
                continue

            response = self.client.put(APIUrl.users_id(user.id), {
                'username': 'andrey',
                'password': '12345',
                'email': 'andr@exemple.com',
                'rang': 'some',
                'group_code': '2'
            })

            self.assertEqual(response.status_code,
                             status.HTTP_404_NOT_FOUND)

    def test_vacations_unknown_list(self):
        response = self.client.get(APIUrl.vacations)
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_vacations_unknown_CRUD(self):
        # Create
        response = self.client.post(APIUrl.vacations, {
            'user': 2,
            'date_start': self.get_date(),
            'date_end': self.get_date(bigger=13),
            'comment_user': 'comment',
            'comment_admin': 'comment',
            'state': 1
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Retrieve
        response = \
            self.client.get(APIUrl.vacations_id(self.user_vacation.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Update
        response = \
            self.client.put(APIUrl.vacations_id(self.user_vacation.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Delete
        response = \
            self.client.delete(APIUrl.vacations_id(self.user_vacation.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vacations_list_by_admin_manager(self):
        for user in [self.admin, self.mger]:
            self.login_e(user)

            response = self.client.get(APIUrl.vacations)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), Vacation.objects.count())

            self.logout_e()

    def test_vacations_list_by_user(self):
        login_user = self.login_user()
        response = self.client.get(APIUrl.vacations)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),
                         Vacation.objects.filter(user=login_user).count())

    def test_vacations_retrieve_by_user(self):
        self.login_user()
        response = \
            self.client.get(APIUrl.vacations_id(self.user_vacation.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vacations_other_retrieve_by_user(self):
        self.login_user()
        response = \
            self.client.get(APIUrl.vacations_id(self.other_user_vacation.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_vacations_retrieve_by_admin_manager(self):
        for user in [self.mger, self.admin]:
            self.login_e(user)

            for vacation in [self.user_vacation, self.other_user_vacation]:
                response = self.client.get(APIUrl.vacations_id(vacation.id))

                self.assertEqual(response.status_code,
                                 status.HTTP_200_OK)

            self.logout_e()

    def test_vacations_delete_by_user_admin_manager(self):
        for user in [self.user, self.mger, self.admin]:
            self.login_e(user)

            response = \
                self.client.delete(APIUrl.vacations_id(self.user_vacation.id))

            self.assertEqual(response.status_code,
                             status.HTTP_405_METHOD_NOT_ALLOWED)

            self.logout_e()

    def test_vacations_update_by_user(self):
        login_user = self.login_user()

        response = \
            self.client.put(APIUrl.vacations_id(self.user_vacation.id), {
                'user': login_user.id,
                'date_start': self.get_date(),
                'date_end': self.get_date(bigger=14),
                'comment_user': 'comment_user',
                'comment_admin': 'comment_admin',
                'state': 1
            })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_other_vacations_update_by_user(self):
        login_user = self.login_user()

        response = \
            self.client.put(APIUrl.vacations_id(self.other_user_vacation.id), {
                'user': login_user.id,
                'date_start': self.get_date(),
                'date_end': self.get_date(bigger=14),
                'comment_user': 'comment_user',
                'comment_admin': 'comment_admin',
                'state': 1
            })

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_by_manager_permissions(self):
        vacations = Vacation.objects.all()
        for vacation in vacations:
            for state in [Vacation.VACATION_NEW,
                          Vacation.VACATION_APPROVED_BY_ADMIN,
                          Vacation.VACATION_REJECTED_BY_ADMIN]:
                response = self.client.put(APIUrl.vacations_id(vacation.id), {
                    'user': vacation.user.id,
                    'date_start': self.get_date(),
                    'date_end': self.get_date(bigger=14),
                    'comment_user': 'comment_manager',
                    'comment_admin': 'comment_manager',
                    'state': state
                })

                self.assertEqual(response.status_code,
                                 status.HTTP_401_UNAUTHORIZED)

    def test_vacations_update_by_manager_REJECTED_AND_APPROVE_MANAGER(self):
        self.login_manager()

        response = \
            self.client.put(APIUrl.vacations_id(self.user_vacation.id), {
                'comment_user': 'comment_manager',
                'comment_admin': 'comment_manager',
                'state': Vacation.VACATION_REJECTED_BY_MANAGER
            })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'],
                         Vacation.VACATION_REJECTED_BY_MANAGER)

        response = \
            self.client.put(APIUrl.vacations_id(self.other_user_vacation.id), {
                'comment_user': 'comment_manager',
                'comment_admin': 'comment_manager',
                'state': Vacation.VACATION_APPROVED_BY_MANAGER
            })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'],
                         Vacation.VACATION_APPROVED_BY_MANAGER)

    def test_vacations_update_first_by_manager_APPR_REJ_BY_ADMIN(self):
        self.login_manager()

        response = \
            self.client.put(APIUrl.vacations_id(self.user_vacation.id), {
                'comment_user': 'comment_manager',
                'comment_admin': 'comment_manager',
                'state': Vacation.VACATION_REJECTED_BY_ADMIN
            })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = \
            self.client.put(APIUrl.vacations_id(self.user_vacation.id), {
                'comment_user': 'comment_manager',
                'comment_admin': 'comment_manager',
                'state': Vacation.VACATION_APPROVED_BY_ADMIN
            })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vacations_update_second_by_manager(self):
        self.login_manager()

        self.user_vacation.state = Vacation.VACATION_APPROVED_BY_MANAGER
        self.user_vacation.save()

        self.other_user_vacation.state = Vacation.VACATION_REJECTED_BY_MANAGER
        self.other_user_vacation.save()

        for vacation in [self.user_vacation, self.other_user_vacation]:
            for state in Vacation.VACATIONS_STATES:
                response = \
                    self.client.put(APIUrl.vacations_id(vacation.id), {
                        'user': vacation.user.id,
                        'date_start': self.get_date(),
                        'date_end': self.get_date(bigger=14),
                        'comment_user': 'comment_manager',
                        'comment_admin': 'comment_manager',
                        'state': state[0]
                    })

                self.assertEqual(response.status_code,
                                 status.HTTP_400_BAD_REQUEST)

        self.user_vacation.state = Vacation.VACATION_APPROVED_BY_ADMIN
        self.user_vacation.save()

        self.other_user_vacation.state = Vacation.VACATION_REJECTED_BY_ADMIN
        self.other_user_vacation.save()

        for vacation in [self.user_vacation, self.other_user_vacation]:
            for state in Vacation.VACATIONS_STATES:
                response = \
                    self.client.put(APIUrl.vacations_id(vacation.id), {
                        'user': vacation.user.id,
                        'date_start': self.get_date(),
                        'date_end': self.get_date(bigger=14),
                        'comment_user': 'comment_manager',
                        'comment_admin': 'comment_manager',
                        'state': state[0]
                    })

                self.assertEqual(response.status_code,
                                 status.HTTP_400_BAD_REQUEST)

    def test_vacations_update_first_by_admin_wrong(self):
        self.login_admin()

        for state in [Vacation.VACATION_APPROVED_BY_MANAGER,
                      Vacation.VACATION_REJECTED_BY_MANAGER]:
            response = \
                self.client.put(APIUrl.vacations_id(self.user_vacation.id), {
                    'user': self.user_vacation.user_id,
                    'date_start': self.get_date(),
                    'date_end': self.get_date(bigger=14),
                    'comment_user': 'comment_new',
                    'comment_admin': 'comment_new',
                    'state': state
                })

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vacations_update_first_by_admin(self):
        self.login_admin()

        response = \
            self.client.put(APIUrl.vacations_id(self.user_vacation.id), {
                'user': self.user_vacation.user_id,
                'date_start': self.get_date(),
                'date_end': self.get_date(bigger=14),
                'comment_user': 'comment_new',
                'comment_admin': 'comment_new',
                'state': Vacation.VACATION_APPROVED_BY_ADMIN
            })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'],
                         Vacation.VACATION_APPROVED_BY_ADMIN)

        response = \
            self.client.put(APIUrl.vacations_id(self.other_user_vacation.id), {
                'user': self.other_user_vacation.user_id,
                'date_start': self.get_date(),
                'date_end': self.get_date(bigger=14),
                'comment_user': 'comment_new',
                'comment_admin': 'comment_new',
                'state': Vacation.VACATION_REJECTED_BY_ADMIN
            })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'],
                         Vacation.VACATION_REJECTED_BY_ADMIN)

    def test_vacations_update_second_by_admin(self):
        self.login_admin()

        self.user_vacation.state = Vacation.VACATION_APPROVED_BY_ADMIN
        self.user_vacation.save()

        self.other_user_vacation.state = Vacation.VACATION_REJECTED_BY_ADMIN
        self.other_user_vacation.save()

        for vacation in [self.user_vacation, self.other_user_vacation]:
            for state in Vacation.VACATIONS_STATES:
                response = self.client.put(APIUrl.vacations_id(vacation.id), {
                    'user': vacation.user.id,
                    'date_start': self.get_date(),
                    'date_end': self.get_date(bigger=14),
                    'comment_user': 'comment_manager',
                    'comment_admin': 'comment_manager',
                    'state': state[0]
                })

                self.assertEqual(response.status_code,
                                 status.HTTP_400_BAD_REQUEST)

    def test_vacations_create_date_start_bigger_date_end(self):
        self.login_user()
        response = self.client.post(APIUrl.vacations, {
            'date_start': self.get_date(bigger=14),
            'date_end': self.get_date()
        })

        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
