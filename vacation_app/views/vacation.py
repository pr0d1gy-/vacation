from datetime import datetime

from rest_framework import mixins

from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from vacation_app.models.vacation import Vacation
from vacation_app.models.employee import Employee
from vacation_app.serializers.vacation import VacationSerializer


class VacationViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      # mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.action == 'list':

            if 'pk' in self.kwargs:
                self.queryset = self.queryset.filter(
                    user_id=self.kwargs['pk']
                )

            date_start = self.request.GET.get('start', None)
            date_end = self.request.GET.get('end', None)

            try:
                if date_start:
                    self.queryset = self.queryset.filter(
                        date_start__gte=datetime.strptime(
                            date_start, '%Y-%m-%d'
                        )
                    )

                if date_end:
                    self.queryset = self.queryset.exclude(
                        date_end__gte=datetime.strptime(
                            date_end, '%Y-%m-%d'
                        )
                    )
            except ValueError:
                pass

        if self.request.user.group_code not in [
            Employee.GADMIN,
            Employee.GMGER
                ]:
            return self.queryset.filter(user=self.request.user)

        return self.queryset
