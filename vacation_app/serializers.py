from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from vacation_app.models import Vacation, Delivery, Employee


class EmployeeSerializer(serializers.ModelSerializer):
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


class VacationSerializerUpdate(VacationSerializer):
    class Meta:
        model = Vacation
        fields = ['state', 'comment_admin']


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'address', 'state', 'action_user', 'action_manager', 'action_admin', 'name']

