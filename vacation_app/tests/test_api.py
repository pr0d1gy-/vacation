from rest_framework.authtoken.models import Token
from rest_framework import status


from rest_framework.test import APITestCase

from vacation_app.models.employee import Employee
from vacation_app.models.vacation import Vacation

from vacation_app.tests.api_url import APIUrl
from vacation_app.tests.api_user import ApiUser
from vacation_app.tests.utils import Utils


class APITests(Utils, ApiUser, APITestCase):

    login = ApiUser()

    def setUp(self):
        super(APITests, self).setUp()

        for user in Employee.objects.all():
            token = Token.objects.create(user=user)
            token.save()

        for user in Employee.objects.all():
            for state in Vacation.VACATIONS_STATES:
                Vacation.objects.create(
                    user=user,
                    date_start=self.get_date(),
                    date_end=self.get_date(bigger=1),
                    comment_user='comment_user',
                    comment_admin='comment_admin',
                    state=state[0]
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

    def test_vacations_unknown_create(self):
        response = self.client.post(APIUrl.vacations, {
            'user': 2,
            'date_start': self.get_date(),
            'date_end': self.get_date(bigger=13),
            'comment_user': 'commetn',
            'comment_admin': 'commetn',
            'state': 1
        })

        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_vacations_unknown_list(self):
        response = self.client.get(APIUrl.vacations)
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_vacations_unknown_retrieve(self):
        vacations = Vacation.objects.all()
        for vacation in vacations:
            response = self.client.get(APIUrl.vacations_id(vacation.id))

            self.assertEqual(response.status_code,
                             status.HTTP_401_UNAUTHORIZED)

    def test_vacations_unknown_delete(self):
        vacations = Vacation.objects.all()
        for vacation in vacations:
            response = self.client.delete(APIUrl.vacations_id(vacation.id))

            self.assertEqual(response.status_code,
                             status.HTTP_401_UNAUTHORIZED)

    def test_vacations_unknown_update(self):
        vacations = Vacation.objects.all()
        for vacation in vacations:
            response = self.client.put(APIUrl.vacations_id(vacation.id))

            self.assertEqual(response.status_code,
                             status.HTTP_401_UNAUTHORIZED)

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
        login_user = self.login_user()
        vacations = Vacation.objects.all()
        for vacation in vacations:
            response = self.client.get(APIUrl.vacations_id(vacation.id))

            if vacation.user == login_user:
                self.assertEqual(response.status_code,
                                 status.HTTP_200_OK)
            else:
                self.assertEqual(response.status_code,
                                 status.HTTP_404_NOT_FOUND)

    def test_vacations_retrieve_by_admin_manager(self):
        vacations = Vacation.objects.all()

        for user in [self.mger, self.admin]:
            self.login_e(user)

            for vacation in vacations:
                response = self.client.get(APIUrl.vacations_id(vacation.id))

                self.assertEqual(response.status_code,
                                 status.HTTP_200_OK)

            self.logout_e()

    def test_vacations_delete_by_user_admin_manager(self):
        vacations = Vacation.objects.all()

        for user in [self.user, self.mger, self.admin]:
            self.login_e(user)

            for vacation in vacations:
                response = \
                    self.client.delete(APIUrl.vacations_id(vacation.id))

                self.assertEqual(response.status_code,
                                 status.HTTP_405_METHOD_NOT_ALLOWED)

            self.logout_e()

    def test_vacations_update_by_user(self):
        login_user = self.login_user()
        vacations = Vacation.objects.all()
        for vacation in vacations:
            response = self.client.put(APIUrl.vacations_id(vacation.id), {
                'user': login_user.id,
                'date_start': self.get_date(),
                'date_end': self.get_date(bigger=14),
                'comment_user': 'commetn_user',
                'comment_admin': 'commetn_admin',
                'state': 1
            })

            if login_user.id == vacation.user_id:
                self.assertEqual(response.status_code,
                                 status.HTTP_400_BAD_REQUEST)
            else:
                self.assertEqual(response.status_code,
                                 status.HTTP_404_NOT_FOUND)

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
                    'comment_user': 'commetn_manager',
                    'comment_admin': 'commetn_manager',
                    'state': state
                })

                self.assertEqual(response.status_code,
                                 status.HTTP_401_UNAUTHORIZED)

    # TODO: FIX
    #
    # def test_vacations_update_first_by_manager_REJECTED_BY_MANAGER(self):
    #     login_user = self.login_manager()
    #     vacations = Vacation.objects.filter(state=Vacation.VACATION_NEW)
    #     for vacation in vacations:
    #         response = self.client.put(APIUrl.vacations_id(vacation.id), {
    #             'comment_user': 'commetn_manager',
    #             'comment_admin': 'commetn_manager',
    #             'state': Vacation.VACATION_REJECTED_BY_MANAGER
    #         })
    #
    #         print response.data
    #
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertEqual(response.data['state'],
    #                          Vacation.VACATION_REJECTED_BY_MANAGER)
    #
    # TODO: FIX
    #
    # def test_vacations_update_first_by_manager_APPROVED_BY_MANAGER(self):
    #     login_user = self.login_manager()
    #     vacations = Vacation.objects.filter(state=Vacation.VACATION_NEW)
    #     for vacation in vacations:
    #         response = self.client.put(APIUrl.vacations_id(vacation.id), {
    #             'comment_user': 'commetn_manager',
    #             'comment_admin': 'commetn_manager',
    #             'state': Vacation.VACATION_APPROVED_BY_MANAGER
    #         })
    #
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertEqual(response.data['state'],
    #                          Vacation.VACATION_APPROVED_BY_MANAGER)

    def test_vacations_update_second_by_manager(self):
        self.login_manager()
        vacations = Vacation.objects.exclude(state=Vacation.VACATION_NEW)
        for vacation in vacations:
            for state in Vacation.VACATIONS_STATES:
                response = self.client.put(APIUrl.vacations_id(vacation.id), {
                    'user': vacation.user.id,
                    'date_start': self.get_date(),
                    'date_end': self.get_date(bigger=14),
                    'comment_user': 'commetn_manager',
                    'comment_admin': 'commetn_manager',
                    'state': state[0]
                })

                self.assertEqual(response.status_code,
                                 status.HTTP_400_BAD_REQUEST)

    # TODO: FIX. wtf??? uniqe error!
    #
    # def test_vacations_update_first_by_admin(self):
    #     login_user = self.login_admin()
    #     vacations = Vacation.objects\
    #         .exclude(state__in=[Vacation.VACATION_REJECTED_BY_ADMIN,
    #                             Vacation.VACATION_APPROVED_BY_ADMIN])
    #
    #     print len(vacations)
    #
    #     for vacation in vacations:
    #         for state in Vacation.VACATIONS_STATES:
    #             response = self.client.get(APIUrl.vacations_id(vacation.id))
    #             print response.data
    #             print vacation.__dict__
    #
    #             response = self.client.put(APIUrl.vacations_id(vacation.id), {
    #                 'user': vacation.user.id,
    #                 'date_start': self.get_date(),
    #                 'date_end': self.get_date(bigger=14),
    #                 'comment_user': 'comment_new',
    #                 'comment_admin': 'comment_new',
    #                 'state': state[0]
    #             })
    #
    #             print response.data
    #
    #             if state[0] in [Vacation.VACATION_APPROVED_BY_ADMIN,
    #                             Vacation.VACATION_REJECTED_BY_ADMIN]:
    #                 self.assertEqual(response.status_code, status.HTTP_200_OK)
    #                 self.assertEqual(response.data['state'], state[0])
    #
    #             else:
    #                 self.assertEqual(response.status_code,
    #                                  status.HTTP_400_BAD_REQUEST)
    #
    #             print 'OK'

    def test_vacations_update_second_by_admin(self):
        self.login_admin()
        vacations = Vacation.objects\
            .filter(state__in=[Vacation.VACATION_REJECTED_BY_ADMIN,
                               Vacation.VACATION_APPROVED_BY_ADMIN])
        for vacation in vacations:
            for state in Vacation.VACATIONS_STATES:
                response = self.client.put(APIUrl.vacations_id(vacation.id), {
                    'user': vacation.user.id,
                    'date_start': self.get_date(),
                    'date_end': self.get_date(bigger=14),
                    'comment_user': 'commetn_manager',
                    'comment_admin': 'commetn_manager',
                    'state': state[0]
                })

                self.assertEqual(response.status_code,
                                 status.HTTP_400_BAD_REQUEST)

    def test_vacations_create_date_start_bigger_date_end(self):
        self.login_user()
        response = self.client.post(APIUrl.vacations, {
            'date_start': self.get_date(),
            'date_end': self.get_date(bigger=14)
        })

        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
