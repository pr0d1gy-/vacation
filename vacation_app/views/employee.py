from django.shortcuts import get_object_or_404

from rest_framework import viewsets

from vacation_app.models import Employee
from vacation_app.serializers import EmployeeSerializer
from vacation_app.decorators import is_manager_or_admin, is_self
from vacation_app.permissins import IsAuthenticatedOrCreateOnly


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrCreateOnly,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @is_manager_or_admin
    def list(self, request, *args, **kwargs):
        return super(EmployeeViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if request.user.group_code == Employee.GUSER:
            self.queryset = self.queryset.filter(username=request.user)
        return super(EmployeeViewSet, self).retrieve(request, *args, **kwargs)

    @is_self
    def update(self, request, *args, **kwargs):
        user = get_object_or_404(Employee, pk=kwargs['pk'])
        request.data['group_code'] = request.user.group_code
        return super(EmployeeViewSet, self).update(request, *args, **kwargs)

    @is_manager_or_admin
    def destroy(self, request, *args, **kwargs):
        return super(EmployeeViewSet, self).destroy(request, *args, **kwargs)
