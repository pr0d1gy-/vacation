from rest_framework import serializers
from vacation_app.models import Vacation
from vacation_app.services import VacationService, ServiceException
from rest_framework.validators import ValidationError


class VacationSerializer(serializers.ModelSerializer):

    user = serializers.CharField(required=False)

    class Meta:
        model = Vacation

        fields = ('id', 'user', 'date_start', 'date_end',
                  'comment_user', 'comment_admin', 'state')

        read_only_fields = ()

    def is_valid(self, raise_exception=False):
        if 'pk' in self.context['view'].kwargs:
            self.Meta.read_only_fields += ('date_start', 'date_end')

        return super(VacationSerializer, self).is_valid(
            raise_exception=raise_exception
        )

    def save(self, **kwargs):
        service = VacationService(user=self.context['request'].user)

        try:
            if 'pk' not in self.context['view'].kwargs:
                return service.add_vacation(
                    self.validated_data['date_start'],
                    self.validated_data['date_end']
                )

            else:
                return service.update_vacation(
                    self._args[0],
                    self.validated_data.get('state', None),
                    self.validated_data.get('comment_admin', None)
                )

        except ServiceException as e:
            raise ValidationError({'error': e.args[0]})
