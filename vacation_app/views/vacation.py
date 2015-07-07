from datetime import datetime
from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from vacation_app.models import Employee, Vacation
from vacation_app.serializers import VacationSerializer


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
        if self.request.user.group_code not in [
            Employee.GADMIN,
            Employee.GMGER
                ]:
            return self.queryset.filter(user=self.request.user)

        return self.queryset

    def list(self, request, *args, **kwargs):
        if 'id_user' in kwargs:
            self.queryset = self.queryset.filter(user=kwargs['id_user'])

        try:
            date_start = request.GET.get('start', None)
            date_end = request.GET.get('end', None)

            if date_start:
                self.queryset = self.queryset.filter(
                    date_start__gte=datetime.strptime(date_start, "%Y-%m-%d")
                )

            if date_end:
                self.queryset = self.queryset.exclude(
                    date_end__gte=datetime.strptime(date_end, "%Y-%m-%d")
                )

        except ValueError:
            return Response({'error': 'Value is not date type'},
                            status=status.HTTP_400_BAD_REQUEST)

        return super(VacationViewSet, self).list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        vacation = get_object_or_404(Vacation, pk=kwargs['pk'])

        if request.user.group_code == Employee.GMGER:
            if vacation.state != [Vacation.VACATION_NEW]:
                return Response({'error': 'value can not be changed'},
                                status=status.HTTP_400_BAD_REQUEST)

            if request.data['state'] not in [
                    Vacation.VACATION_APPROVED_BY_MANAGER,
                    Vacation.VACATION_REJECTED_BY_MANAGER
                    ]:
                return Response({'error': 'value is not valid for manager'},
                                status=status.HTTP_400_BAD_REQUEST)

        if request.user.group_code == Employee.GADMIN:
            if vacation.state in [
                    Vacation.VACATION_APPROVED_BY_ADMIN,
                    Vacation.VACATION_REJECTED_BY_ADMIN
                    ]:
                return Response({'error': 'value can not be changed'},
                                status=status.HTTP_400_BAD_REQUEST)

            if request.data['state'] not in [
                    Vacation.VACATION_APPROVED_BY_ADMIN,
                    Vacation.VACATION_REJECTED_BY_ADMIN
                    ]:
                return Response({'error': 'value is not valid for admin'},
                                status=status.HTTP_400_BAD_REQUEST)

        return super(VacationViewSet, self).update(request, *args, **kwargs)
