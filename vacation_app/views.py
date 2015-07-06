from datetime import datetime
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template.context import RequestContext
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from vacation_app.models import Employee, Delivery, Vacation
from vacation_app.serializers import EmployeeSerializer, VacationSerializer, VacationSerializerUpdate, DeliverySerializer
from vacation_app.decorators import get_for_user, is_manager_or_admin, is_self
from vacation_app.permissins import IsAdminEmployee, IsAuthenticatedOrCreateOnly

def index(request, template_name="index.html"):
    response = render_to_response(template_name, context_instance=RequestContext(request))
    return response


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


class VacationViewSet(
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    # mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer

    def dispatch(self, request, *args, **kwargs):
        return super(VacationViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        request.data['state'] = 1
        return super(VacationViewSet, self).create(request, *args, **kwargs)

    @get_for_user
    def list(self, request, *args, **kwargs):
        if kwargs.has_key('id_user'):
            self.queryset = self.queryset.filter(user=kwargs['id_user'])
        else:
            try:
                if request.QUERY_PARAMS.has_key('start'):
                    start_data = datetime.strptime(request.QUERY_PARAMS['start'], "%Y-%m-%d")
                    self.queryset = self.queryset.filter(date_start__gte=start_data)
                if request.QUERY_PARAMS.has_key('end'):
                    end_data = datetime.strptime(request.QUERY_PARAMS['end'], "%Y-%m-%d")
                    self.queryset = self.queryset.exclude(date_end__gte=end_data)
            except ValueError:
                return Response({'error': 'value is not date type'}, status=status.HTTP_400_BAD_REQUEST)

        return super(VacationViewSet, self).list(request, *args, **kwargs)

    @get_for_user
    def retrieve(self, request, *args, **kwargs):
        return super(VacationViewSet, self).retrieve(request, *args, **kwargs)

    @is_manager_or_admin
    def update(self, request, *args, **kwargs):
        vacation = get_object_or_404(Vacation, pk=kwargs['pk'])
        self.serializer_class = VacationSerializerUpdate
        if request.user.group_code == Employee.GMGER:
            if vacation.state != [Vacation.VACATION_NEW]:
                return Response({'error': 'value can not be changed'}, status=status.HTTP_400_BAD_REQUEST)
            if not request.data['state'] in [Vacation.VACATION_APPROVED_BY_MANAGER, Vacation.VACATION_REJECTED_BY_MANAGER]:
                return Response({'error': 'value is not valid for manager'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.group_code == Employee.GADMIN:
            if vacation.state in [Vacation.VACATION_APPROVED_BY_ADMIN, Vacation.VACATION_REJECTED_BY_ADMIN]:
                return Response({'error': 'value can not be changed'}, status=status.HTTP_400_BAD_REQUEST)
            if not request.data['state'] in [Vacation.VACATION_APPROVED_BY_ADMIN, Vacation.VACATION_REJECTED_BY_ADMIN]:
                return Response({'error': 'value is not valid for admin'}, status=status.HTTP_400_BAD_REQUEST)
        return super(VacationViewSet, self).update(request, *args, **kwargs)


class DeliveryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminEmployee,)
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
