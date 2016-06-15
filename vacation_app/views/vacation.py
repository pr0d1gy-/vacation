from datetime import datetime, timedelta

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
    paginate_by = 0
    serializer_class = VacationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.action == 'list':

            if 'pk' in self.kwargs:
                self.queryset = self.queryset.filter(
                    user_id=self.kwargs['pk']
                )

            month = self.request.GET.get('month', None)
            year = self.request.GET.get('year', None)

            if month:
                now = datetime.now()

                try:
                    month = int(month)
                    if 1 > month or month > 12:
                        raise ValueError
                except (ValueError, TypeError):
                    month = now.month

                try:
                    year = int(year)
                except (ValueError, TypeError):
                    year = now.year

                start = (
                    datetime.strptime('%s-%s' % (year, month), '%Y-%m') -
                    timedelta(days=10)
                )

                if month == 12:
                    month = 0
                    year += 1

                end = (
                    datetime.strptime('%s-%s' % (year, month + 1), '%Y-%m') +
                    timedelta(days=10)
                )

                self.queryset = self.queryset.filter(
                    date_start__gte=start
                )

                self.queryset = self.queryset.filter(
                    date_end__lte=end
                )

            self.queryset = self.queryset.order_by('date_start')

        if self.request.user.group_code not in [
            Employee.GADMIN,
            Employee.GMGER
                ]:
            return self.queryset.filter(user=self.request.user)

        return self.queryset
