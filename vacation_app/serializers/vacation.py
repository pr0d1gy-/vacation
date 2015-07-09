from rest_framework import serializers
from vacation_app.models import Vacation
from vacation_app.services import VacationService, ServiceException
from rest_framework.validators import ValidationError


class VacationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vacation

        fields = ('id', 'user', 'date_start', 'date_end',
                  'comment_user', 'comment_admin', 'state')

        read_only_fields = ('user',)

    def save(self, **kwargs):
        service = VacationService(user=self.context['request'].user)

        try:
            if 'pk' not in self.context['view'].kwargs:
                return service.add_vacation(**self.validated_data)
            else:
                return service.update_vacation(self._args[0],
                                               **self.validated_data)
        except ServiceException as e:
            raise ValidationError(e.args[0])
