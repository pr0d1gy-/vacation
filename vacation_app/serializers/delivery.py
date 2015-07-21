from rest_framework import serializers
from vacation_app.models import Delivery


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'address', 'state', 'action_user',
                  'action_manager', 'action_admin', 'name']

    def is_valid(self, raise_exception=False):
        if self.context['request'].method == 'PUT':
            self.fields.fields['address'].required = False
            self.fields.fields['name'].required = False
        return super(DeliverySerializer, self).is_valid(raise_exception)
