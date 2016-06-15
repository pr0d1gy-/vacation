from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from vacation_app.views.employee import Employee


class TokenAuthWithIdNameGroup(ObtainAuthToken):

    def post(self, request):
        response = super(TokenAuthWithIdNameGroup, self).post(request)
        token = Token.objects.get(key=response.data['token'])
        user = Employee.objects.get(id=token.user_id)
        response.data.update({
            'id': user.id,
            'email': user.email,
            'group_code': user.group_code
        })

        return response
