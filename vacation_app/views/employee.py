from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import detail_route

from vacation_app.models import Employee
from vacation_app.serializers import EmployeeSerializer
from vacation_app.decorators import is_manager_or_admin, is_self
from vacation_app.permissins import IsAuthenticatedOrCreateOnly
from vacation_app.views.vacation import VacationViewSet


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrCreateOnly,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        if self.request.method == 'PUT':
            if self.request.user.id != int(self.kwargs['pk']):
                Response({'error': 'Only for self'}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.queryset
        
        # if self.request.user.group_code == Employee.GUSER:
        #     queryset = queryset.filter(username=self.request.user)

        return queryset

    @is_self
    def update(self, request, *args, **kwargs):
        user = get_object_or_404(Employee, pk=kwargs['pk'])
        request.data['group_code'] = request.user.group_code
        return super(EmployeeViewSet, self).update(request, *args, **kwargs)

    @is_manager_or_admin
    def destroy(self, request, *args, **kwargs):
        return super(EmployeeViewSet, self).destroy(request, *args, **kwargs)

    @detail_route()
    def vacations(self, request, *args, **kwargs):
        return VacationViewSet.as_view({'get': 'list'})(request, *args, **kwargs)
