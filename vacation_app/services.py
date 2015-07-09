from django.core.exceptions import ValidationError

from vacation_app.models import Vacation
from vacation_app.models import Employee


class ServiceException(Exception):
    pass


class VacationService(object):

    def __init__(self, **kwargs):
        self.user = kwargs.pop('user', None)
        self.vacation = kwargs.pop('vacation', None)

    def add_vacation(self, date_start, date_end, comment_user=None):
        try:
            self.vacation = Vacation(
                user=self.user,
                date_start=date_start,
                date_end=date_end,
                comment_user=comment_user
            ).save()
        except ValidationError as e:
            raise ServiceException(e.args[0])

        return self.vacation

    def update_vacation(self, vacation, state, comment_admin=None):
        if not state:
            raise ServiceException('State is invalid.')

        if self.user.group_code == Employee.GUSER:
            raise ServiceException('You have not permissions '
                                   'for update vacation.')

        self.vacation = vacation

        if comment_admin:
            if self.user.group_code != Employee.GADMIN:
                raise ServiceException('`Comment admin` field only'
                                       ' for admin.')

            self.vacation.comment_admin = comment_admin

        if state in [
                Vacation.VACATION_APPROVED_BY_ADMIN,
                Vacation.VACATION_APPROVED_BY_MANAGER
                ]:
            self.approve_vacation(commit=False)

        elif state in [
                Vacation.VACATION_REJECTED_BY_ADMIN,
                Vacation.VACATION_REJECTED_BY_MANAGER
                ]:
            self.reject_vacation(commit=False)

        else:
            raise ServiceException('State is wrong.')

        self.vacation.save()

        return self.vacation

    def approve_vacation(self, commit=False):
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

        return self.vacation

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

        return self.vacation

    def _check_update_for_manager(self):
        if self.vacation.state != Vacation.VACATION_NEW:
            raise ServiceException('Vacation can not be changed.')

    def _check_update_form_admin(self):
        if self.vacation.state in [
            Vacation.VACATION_APPROVED_BY_ADMIN,
            Vacation.VACATION_REJECTED_BY_ADMIN
                ]:
            raise ServiceException('Vacation can not be changed.')
