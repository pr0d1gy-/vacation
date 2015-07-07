from django.shortcuts import get_object_or_404

from rest_framework import status

from vacation_app.models import Vacation
from vacation_app.models import Employee


class VacationService(object):

    errors = None
    status = None

    def create(self):
        pass

    def update(self, request, *args, **kwargs):
        self.errors = dict()
        self.status = None

        try:
            vacation = Vacation.objects.get(pk=kwargs['pk'])
        except Vacation.DoesNotExist:
            self.errors['error'] = 'Vacation was not found.'
            self.status = status.HTTP_404_NOT_FOUND

            return False

        if request.user.group_code == Employee.GMGER:
            if vacation.state != [Vacation.VACATION_NEW]:
                self.errors['error'] = 'Value can not be changed.'
                self.status = status.HTTP_400_BAD_REQUEST

                return False

            if request.data['state'] not in [
                    Vacation.VACATION_APPROVED_BY_MANAGER,
                    Vacation.VACATION_REJECTED_BY_MANAGER
                    ]:
                self.errors['error'] = 'Value is not valid for manager.'
                self.status = status.HTTP_400_BAD_REQUEST

                return False

        if request.user.group_code == Employee.GADMIN:
            if vacation.state in [
                    Vacation.VACATION_APPROVED_BY_ADMIN,
                    Vacation.VACATION_REJECTED_BY_ADMIN
                    ]:
                self.errors['error'] = 'Value can not be changed.'
                self.status = status.HTTP_400_BAD_REQUEST

                return False

            if request.data['state'] not in [
                    Vacation.VACATION_APPROVED_BY_ADMIN,
                    Vacation.VACATION_REJECTED_BY_ADMIN
                    ]:
                self.errors['error'] = 'Value is not valid for admin.'
                self.status = status.HTTP_400_BAD_REQUEST

                return False

        if request.user.group_code == Employee.GUSER:
            if int(request.data['state']) != vacation.state:
                self.errors['error'] = 'No permission to change state.'
                self.status = status.HTTP_403_FORBIDDEN

                return False

        return True
