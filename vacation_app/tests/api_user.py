from rest_framework.authtoken.models import Token

from vacation_app.models.employee import Employee


class ApiUser(object):

    def login_user(self):
        if hasattr(self, 'user'):
            user = self.user
        else:
            user = Employee.objects.filter(group_code=Employee.GMGER).first()

        user = Employee.objects.filter(group_code=Employee.GUSER).first()
        token = Token.objects.get(user=user)
        self.client.force_authenticate(user=user, token=token.key)

        return user

    def login_manager(self):
        if hasattr(self, 'mger'):
            user = self.mger
        else:
            user = Employee.objects.filter(group_code=Employee.GMGER).first()

        token = Token.objects.get(user=user)

        self.client.force_authenticate(user=user, token=token.key)

        return user

    def login_admin(self):
        if hasattr(self, 'admin'):
            user = self.admin
        else:
            user = Employee.objects.filter(group_code=Employee.GMGER).first()

        user = Employee.objects.filter(group_code=Employee.GADMIN).first()
        token = Token.objects.get(user=user)
        self.client.force_authenticate(user=user, token=token.key)

        return user

    def login_e(self, user):
        token = Token.objects.get(user=user)
        self.client.force_authenticate(user=user, token=token.key)

        return user

    def logout_e(self):
        self.client.force_authenticate(user=None, token=None)
