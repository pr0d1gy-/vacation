from rest_framework import serializers
from rest_framework.validators import ValidationError

from vacation_app.models import Vacation
from vacation_app.services import VacationService, ServiceException
from employee import EmployeeSerializer


class VacationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = Vacation

        fields = ('id', 'user', 'date_start', 'date_end',
                  'comment_user', 'comment_admin', 'state')

        read_only_fields = ()

    def _get_model_fields(self, field_names, declared_fields, extra_kwargs):
        if self.context['request'].method == 'GET':
            declared_fields['user'] = EmployeeSerializer()
        return super(VacationSerializer, self)._get_model_fields(field_names, declared_fields, extra_kwargs)

    def is_valid(self, raise_exception=False):
        if 'pk' in self.context['view'].kwargs:
            self.Meta.read_only_fields += ('date_start', 'date_end')

        return super(VacationSerializer, self).is_valid(
            raise_exception=raise_exception
        )

    def create(self, validated_data):
        service = VacationService(user=self.context['request'].user)
        try:
            return service.add_vacation(
                validated_data['date_start'],
                validated_data['date_end'],
                validated_data.get('comment_user', None)
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
