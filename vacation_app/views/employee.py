from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from vacation_app.models import Employee
from vacation_app.serializers import EmployeeSerializer
from vacation_app.decorators import is_manager_or_admin, is_self
from vacation_app.permissions import IsAuthenticatedOrCreateOnly
from vacation_app.views.vacation import VacationViewSet


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrCreateOnly,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        if self.request.method == 'PUT':
            if str(user.id) != self.kwargs['pk']:
                return
        if self.request.method == 'DELETE':
            if user.group_code != Employee.GADMIN:
                return
        if self.request.user.group_code == Employee.GUSER:
            queryset = queryset.filter(username=self.request.user)
        return queryset

    @detail_route()
    def vacations(self, request, *args, **kwargs):
        return VacationViewSet.as_view({'get': 'list'})(request, *args, **kwargs)