from rest_framework import serializers
from vacation_app.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'password',
                  'rang', 'group_code']

    def create(self, validated_data):
        user = Employee.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            rang=validated_data['rang'],
            group_code=Employee.GUSER,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super(EmployeeSerializer, self).update(instance,
                                                      validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class EmployeeSerializerUpdate(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'password']