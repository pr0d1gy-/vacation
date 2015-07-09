from rest_framework import viewsets

from vacation_app.models.delivery import Delivery
from vacation_app.serializers.delivery import DeliverySerializer
from vacation_app.permissions import IsAdminEmployee


class DeliveryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminEmployee,)
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
