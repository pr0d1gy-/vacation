from rest_framework import serializers
from vacation_app.models import Delivery


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'address', 'state', 'action_user',
                  'action_manager', 'action_admin', 'name']

