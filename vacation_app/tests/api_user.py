from rest_framework.authtoken.models import Token

from vacation_app.models.employee import Employee


class ApiUser(object):

    def login_user(self):
        user = Employee.objects.all().filter(group_code=Employee.GUSER).first()
        token = Token.objects.get(user=user)
        self.client.force_authenticate(user=user, token=token.key)
        return user

    def login_manager(self):
        user = Employee.objects.all().filter(group_code=Employee.GMGER).first()
        token = Token.objects.get(user=user)
        self.client.force_authenticate(user=user, token=token.key)
        return user

    def login_admin(self):
        user = Employee.objects.all().filter(group_code=Employee.GADMIN).first()
        token = Token.objects.get(user=user)
        self.client.force_authenticate(user=user, token=token.key)
        return user

    def login_e(self, user):
        token = Token.objects.get(user=user)
        self.client.force_authenticate(user=user, token=token.key)
        return user

    def logout_e(self):
        self.client.force_authenticate(user=None, token=None)
