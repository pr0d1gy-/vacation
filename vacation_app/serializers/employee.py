from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from vacation_app.models import Employee


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['write_only'] = True
        super(PasswordField, self).__init__(*args, **kwargs)

    def run_validation(self, data):
        if self.context['request'].method == 'PUT':
            self.required = False
        value = super(PasswordField, self).run_validation(data)
        return make_password(value)


class EmployeeSerializer(serializers.ModelSerializer):
    password = PasswordField()

    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'password', 'rang', 'group_code',
                  'first_name', 'last_name']
        read_only_fields = ['group_code']

    def is_valid(self, raise_exception=False):

        return super(EmployeeSerializer, self).is_valid(raise_exception)
