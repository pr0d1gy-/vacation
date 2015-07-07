from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from vacation_app.models import Employee


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['write_only'] = True
        super(PasswordField, self).__init__(*args, **kwargs)

    def run_validation(self, data):
        value = super(PasswordField, self).run_validation(data)
        return make_password(value)


class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = PasswordField(required=False)

    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'password', 'rang', 'group_code']
        read_only_fields = ['group_code']

    def update(self, instance, validated_data):
        return super(EmployeeSerializer, self).update(instance, validated_data)