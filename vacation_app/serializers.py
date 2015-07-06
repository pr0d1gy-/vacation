from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from vacation_app.models import Vacation, Delivery, Employee


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['write_only'] = True
        super(PasswordField, self).__init__(*args, **kwargs)

    def from_native(self, value):
        return make_password(value)


class EmployeeSerializer(serializers.ModelSerializer):
    # password = PasswordField(required=False, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)

    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'password', 'rang', 'group_code']

    def create(self, validated_data):
        user = Employee.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            rang=validated_data['rang'],
            group_code=0,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super(EmployeeSerializer, self).update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = ['id', 'user', 'date_start', 'date_end', 'comment_user', 'comment_admin', 'state']

    # def update(self, instance, validated_data):
    #     vacation = super(VacationSerializer, self).update(instance, validated_data)
    #     instance.save()
    #     return instance

class VacationSerializerUpdate(VacationSerializer):
    class Meta:
        model = Vacation
        fields = ['state']

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'address', 'state', 'action_user', 'action_manager', 'action_admin', 'name']

