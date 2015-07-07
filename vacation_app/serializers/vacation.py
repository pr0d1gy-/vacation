from rest_framework import serializers
from vacation_app.models import Vacation


class VacationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vacation
        fields = ['id', 'user', 'date_start', 'date_end',
                  'comment_user', 'comment_admin', 'state']


class VacationSerializerUpdate(VacationSerializer):
    class Meta:
        model = Vacation
        fields = ['state', 'comment_admin']