from django.core.exceptions import ValidationError

from vacation_app.models import Vacation
from vacation_app.models import Employee


class ServiceException(Exception):
    pass


class VacationService(object):

    def __init__(self, **kwargs):
        self.user = kwargs.pop('user', None)
        self.vacation = kwargs.pop('vacation', None)

    def add_vacation(self, **kwargs):
        for var in kwargs:
            if var not in [
                'date_start',
                'date_end',
                'state',
                'comment_user'
                    ]:
                raise ServiceException('Wrong parameter: %s.' % var)

        if 'state' in kwargs and \
                kwargs['state'] != Vacation.VACATION_NEW:
            raise ServiceException('Vacation must be created'
                                   ' with state `NEW`.')

        vacation_params = dict()
        vacation_params['date_start'] = kwargs.pop('date_start', None)
        vacation_params['date_end'] = kwargs.pop('date_end', None)
        vacation_params['comment_user'] = kwargs.pop('comment_user', None)
        vacation_params['user'] = self.user
        vacation_params['state'] = Vacation.VACATION_NEW

        try:
            self.vacation = Vacation(**vacation_params).save()
        except ValidationError as e:
            raise ServiceException(e.args[0])

        return self.vacation

    def update_vacation(self, vacation, **kwargs):
        for var in kwargs:
            if var not in [
                'comment_admin',
                'state'
                    ]:
                raise ServiceException('Wrong parameter: %s.' % var)

        if self.user.group_code == Employee.GUSER:
            raise ServiceException('You have not permissions '
                                   'for update vacation.')

        if not vacation or \
                not isinstance(vacation, Vacation):
            raise ServiceException('Vacation was not found.')

        self.vacation = vacation

        comment_admin = kwargs.pop('comment_admin', None)
        if comment_admin:
            if self.user.group_code != Employee.GADMIN:
                raise ServiceException('`Comment admin` field only'
                                       ' for admin.')

            self.vacation.comment_admin = comment_admin

        if 'state' in kwargs and \
                kwargs['state'] != self.vacation.state:
            if kwargs['state'] in [
                    Vacation.VACATION_APPROVED_BY_ADMIN,
                    Vacation.VACATION_APPROVED_BY_MANAGER
                    ]:
                self.approve_vacation(commit=False)

            elif kwargs['state'] in [
                    Vacation.VACATION_REJECTED_BY_ADMIN,
                    Vacation.VACATION_REJECTED_BY_MANAGER
                    ]:
                self.reject_vacation(commit=False)

            else:
                raise ServiceException('State is wrong.')
        else:
            if not comment_admin:
                raise ServiceException('Missing parameters.')

        self.vacation.save()

        return self.vacation

    def approve_vacation(self, commit=True):
        if not self.vacation or \
                not isinstance(self.vacation, Vacation):
            raise ServiceException('Vacation was not found.')

        if self.user.group_code == Employee.GADMIN:
            self._check_update_form_admin()

            self.vacation.state = Vacation.VACATION_APPROVED_BY_ADMIN

        if self.user.group_code == Employee.GMGER:
            self._check_update_for_manager()

            self.vacation.state = Vacation.VACATION_APPROVED_BY_MANAGER

        if commit:
            self.vacation.save()

    def reject_vacation(self, commit=False):
        if not self.vacation or \
                not isinstance(self.vacation, Vacation):
            raise ServiceException('Vacation was not found.')

        if self.user.group_code == Employee.GADMIN:
            self._check_update_form_admin()

            self.vacation.state = Vacation.VACATION_REJECTED_BY_ADMIN

        if self.user.group_code == Employee.GMGER:
            self._check_update_for_manager()

            self.vacation.state = Vacation.VACATION_REJECTED_BY_MANAGER

        if commit:
            self.vacation.save()

    def _check_update_for_manager(self):
        if self.vacation.state != Vacation.VACATION_NEW:
            raise ServiceException('Vacation can not be changed.')

    def _check_update_form_admin(self):
        if self.vacation.state in [
            Vacation.VACATION_APPROVED_BY_ADMIN,
            Vacation.VACATION_REJECTED_BY_ADMIN
                ]:
            raise ServiceException('Vacation can not be changed.')
