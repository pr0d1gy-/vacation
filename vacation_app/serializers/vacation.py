from rest_framework import serializers
from vacation_app.models import Vacation


class VacationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vacation

        fields = ('id', 'user', 'date_start', 'date_end',
                  'comment_user', 'comment_admin', 'state')

        read_only = ('id', 'user')

    def __init__(self, *args, **kwargs):
        self.action = kwargs['context']['view'].action

        if self.action == 'create':
            self.Meta.read_only += ('comment_user', 'comment_admin', 'state')

        if self.action == 'update':
            self.Meta.read_only += ('date_start', 'date_end', 'comment_user')

        super(VacationSerializer, self).__init__(*args, **kwargs)

    def is_valid(self, raise_exception=False):
        if self.action == 'create':
            self.initial_data['user'] = self.context['request'].user.pk

        super(VacationSerializer, self).is_valid(
            raise_exception=raise_exception
        )
