from rest_framework import viewsets

from vacation_app.models import Delivery
from vacation_app.serializers import DeliverySerializer
from vacation_app.permissins import IsAdminEmployee


class DeliveryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminEmployee,)
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
