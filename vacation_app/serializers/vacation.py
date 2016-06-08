from rest_framework import serializers
from rest_framework.validators import ValidationError

from vacation_app.models import Vacation
from vacation_app.services import VacationService, ServiceException
from employee import EmployeeSerializer


class VacationSerializer(serializers.ModelSerializer):

    user = EmployeeSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    possible_days = serializers.SerializerMethodField()

    class Meta:
        model = Vacation

        fields = ('id', 'user', 'date_start', 'date_end', 'possible_days',
                  'comment_user', 'comment_admin', 'state')

        read_only_fields = ('possible_days',)

    @staticmethod
    def get_possible_days(obj):
        print obj.VACATION_DAY_LIMIT
        print obj.get_vacations_days_by_user()
        return obj.VACATION_DAY_LIMIT - obj.get_vacations_days_by_user()

    def _get_model_fields(self, field_names, declared_fields, extra_kwargs):
        if self.context['request'].method == 'GET':
            declared_fields['user'] = EmployeeSerializer()
        return super(VacationSerializer, self)._get_model_fields(
            field_names, declared_fields, extra_kwargs)

    def is_valid(self, raise_exception=False):
        if self.context['request'].method == 'PUT':
            self.fields['date_start'].required = False
            self.fields['date_end'].required = False

        return super(VacationSerializer, self).is_valid(
            raise_exception=raise_exception
        )

    def create(self, validated_data):
        service = VacationService(user=self.context['request'].user)
        try:
            return service.add_vacation(
                date_start=validated_data['date_start'],
                date_end=validated_data['date_end'],
                comment_user=validated_data.get('comment_user', None)
            )
        except ServiceException as e:
            raise ValidationError({'error': e.args[0]})

    def update(self, instance, validated_data):
        service = VacationService(user=self.context['request'].user)
        try:
            return service.update_vacation(
                self.instance,
                self.validated_data.get('state', None),
                self.validated_data.get('comment_admin', None)
            )
        except ServiceException as e:
            raise ValidationError({'error': e.args[0]})
