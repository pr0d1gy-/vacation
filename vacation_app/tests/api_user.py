from rest_framework.authtoken.models import Token

from vacation_app.models.employee import Employee


class ApiUser(object):

    def __get_user(self, user_type, is_login=False):
        user_type_map = {
            'user': Employee.GUSER,
            'mger': Employee.GMGER,
            'admin': Employee.GADMIN
        }

        group = user_type_map[user_type]
        user = getattr(self, user_type)

        if not user:
            user = Employee.objects.filter(group_code=group).first()

        if is_login:
            self.__login(user, self.__get_token(user).key)

        return user

    def __get_token(self, user):
        group_map = ['user_token', 'mger_token', 'admin_token']
        token = getattr(self, group_map[int(user.group_code) - 1])

        if not token:
            token = Token.objects.get(user=user)

        return token

    def __login(self, user, token_key):
        self.client.force_authenticate(user=user, token=token_key)

    def login_user(self):
        return self.__get_user('user', True)

    def login_manager(self):
        return self.__get_user('mger', True)

    def login_admin(self):
        return self.__get_user('admin', True)

    def login_e(self, user):
        self.__login(user, self.__get_token(user).key)

    def logout_e(self):
        self.__login(None, None)
