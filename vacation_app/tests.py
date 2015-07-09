import datetime
from django.core import mail
from django.http import response
from django.utils import timezone
from django.test import TestCase, Client
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APIRequestFactory, APIClient, APITestCase, force_authenticate

from vacation_app.models.employee import Employee
from vacation_app.models.vacation import Vacation

# ./manage.py test -v 3
# python -Wall manage.py test -v 3

class APIUrl(object):
    vacations = '/api/vacations/'
    users = '/api/users/'
    mails = '/api/mails/'

    def vacations_id(self, id):
        return self.vacations + str(id) + '/'

    def users_id(self, id):
        return self.users + str(id) + '/'

    def mails_id(self, id):
        return self.mails + str(id) + '/'


class ApiUser(object):
    def login_user(self):
        user = Employee.objects.all().filter(group_code=Employee.GUSER).first()
        self.user = user
        token = Token.objects.get(user=user)
        self.client.force_authenticate(user=user, token=token.key)


class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail('Subject here', 'Here is the message.',
            'arseniysychev@gmail.com', ['arseniys@ua.fm'],
            fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')


# class ModelTest(TestCase):
#
#     def setUp(self):
#         user = Employee.objects.create(
#             username='user',
#             email='user@host.ua',
#             rang='develop',
#             group_code=Employee.GUSER
#         )
#         user.set_password('12345')
#         user.save()
#         mger = Employee.objects.create(
#             username='manager',
#             email='manager@host.ua',
#             rang='manager',
#             group_code=Employee.GMGER
#         )
#         mger.set_password('12345')
#         mger.save()
#         admin = Employee.objects.create(
#             username='admin',
#             password='12345',
#             email='admin@host.ua',
#             rang='administrator',
#             group_code=Employee.GADMIN
#         )
#         admin.set_password('12345')
#         admin.save()
#
#     def test_vacation_date_start_bigger_date_end(self):
#         client = Client()
#         client.login(username='user', password='12345')
#         user = Employee.objects.get(username='user')
#         date_start = datetime.datetime.strptime('2015-07-03', "%Y-%m-%d").date()
#         date_end = datetime.datetime.strptime('2015-07-02', "%Y-%m-%d").date()
#         vacation = Vacation(
#             date_start=date_start,
#             date_end=date_end
#         )
#         vacation.save()
#         print Vacation.objects.all()
#         self.assertEqual(Vacation.objects.filter(pk=vacation.id).exists(), False)
#
#     def test_vacation_delta_dates_bigger_14(self):
#         user = Employee.objects.get(username='user')
#         date_start = datetime.datetime.strptime('2015-07-01', "%Y-%m-%d").date()
#         date_end = datetime.datetime.strptime('2015-07-16', "%Y-%m-%d").date()
#         vacation = Vacation.objects.create(
#             user=user,
#             date_start=date_start,
#             date_end=date_end
#         )
#         self.assertEqual(Vacation.objects.filter(pk=vacation.id).exists(), False)
#
#     def test_update_by_manager(self):
#         client = Client()
#         client.login(username='manager', password='12345')


class APITestsUsers(ApiUser, APITestCase):
    api = APIUrl()
    login = ApiUser()

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

        for user in Employee.objects.all():
            token = Token.objects.create(user=user)
            token.save()

        # print Employee.objects.all()

    def test_user_create(self):
        response = self.client.post(self.api.users, {
            'username': 'andrey',
            'password': '12345',
            'email': 'andr@exemple.com',
            'rang': 'some',
            'group_code': '2'
        })
        self.assertEqual(response.data['group_code'], Employee.GUSER)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_users_unknown_list(self):
        response = self.client.get(self.api.users)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_unknown_retrieve(self):
        for user in Employee.objects.all():
            response = self.client.get(self.api.users_id(user.id))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_unknown_delete(self):
        for user in Employee.objects.all():
            response = self.client.delete(self.api.users_id(user.id))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_unknown_update(self):
        for user in Employee.objects.all():
            response = self.client.put(self.api.users_id(user.id), {
                'username': 'andrey',
                'password': '12345',
                'email': 'andr@exemple.com',
                'rang': 'some',
                'group_code': '2'
            })
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_user_list(self):
        self.login_user()
        response = self.client.get(self.api.users)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_users_user_retrieve_self(self):
        self.login_user()
        response = self.client.get(self.api.users_id(self.user.id))
        data = {key: self.user.__getattribute__(key) for (key) in response.data.keys()}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_users_user_retrieve_other(self):
        self.login_user()
        for user in Employee.objects.all():
            if user.id == self.user.id:
                continue
            response = self.client.get(self.api.users_id(user.id))
            # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_user_delete(self):
        self.login_user()
        for user in Employee.objects.all():
            response = self.client.delete(self.api.users_id(user.id))
            # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_user_update_self(self):
        self.login_user()
        response = self.client.put(self.api.users_id(self.user.id), {
                'username': 'andrey',
                'password': '12345',
                'email': 'andr@exemple.com',
                'rang': 'some',
                'group_code': '2'
            })
        self.assertEqual(response.data['group_code'], Employee.GUSER)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_user_update_other(self):
        self.login_user()
        for user in Employee.objects.all():
            if user.id == self.user.id:
                continue
            response = self.client.put(self.api.users_id(user.id), {
                'username': 'andrey',
                'password': '12345',
                'email': 'andr@exemple.com',
                'rang': 'some',
                'group_code': '2'
            })
            # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_vacations_unknown_create(self):
        response = self.client.post(self.api.users, {
            "user": 1,
            "date_start": "2015-07-02",
            "date_end": "2015-07-03",
            "comment_user": "commetn",
            "comment_admin": "commetn",
            "state": 2
        })
        print response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
