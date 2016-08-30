import logging

from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.utils.translation import ugettext as _

from celery.task import task


log = logging.getLogger()


@task(ignore_result=True, name='notification_update_vacations')
def notification_update_vacations(vacation_id):
    from vacation_app.models import Delivery, Vacation
    from _vacation_project.settings import FROM_EMAIL

    try:
        vacation = Vacation.objects.get(pk=vacation_id)
        is_notify_user = False
    except Vacation.DoesNotExist:
        log.error('Vacation with `%s` id was not found.' % vacation_id)
        return None

    deliveries = Delivery.objects.filter(state=True)

    if vacation.state in [Vacation.VACATION_REJECTED_BY_ADMIN,
                          Vacation.VACATION_APPROVED_BY_ADMIN]:
        # Filter delivery for admin's changes
        deliveries = deliveries.filter(action_admin=True)
        is_notify_user = True

    elif vacation.state in [Vacation.VACATION_APPROVED_BY_MANAGER,
                            Vacation.VACATION_REJECTED_BY_MANAGER]:
        # Filter delivery for manager's changes
        deliveries = deliveries.filter(action_manager=True)

    else:
        log.warning('Unknown state `%s` in vacation `%s`.' % (
            vacation.state,
            vacation.pk
        ))
        return None

    if is_notify_user:
        # Send notification to User
        vacation.user.email_user(
            subject=_('Vacations'),
            message=_('Your have result for you vacation'),
            from_email=FROM_EMAIL
        )

    recipient_list = []
    for delivery in deliveries:
        recipient_list.append(delivery.address)

    by_admin = _('by admin')
    by_manager = _('by manager')

    return send_mail(
        subject=_('Vacation created by %s was updated %s ') % (
            vacation.user.get_full_name(),
            by_admin if is_notify_user else by_manager
        ),
        message=_('Vacation %s - %s for %s is updated') % (
            vacation.user.get_full_name(),
            vacation.date_start.strftime('%Y-%m-%d'),
            vacation.date_end.strftime('%Y-%m-%d'),
        ),
        from_email=FROM_EMAIL,
        recipient_list=recipient_list
    )


@task(ignore_result=True, name='notification_create_vacations')
def notification_create_vacations(vacation_id):
    from vacation_app.models import Delivery, Vacation
    from _vacation_project.settings import FROM_EMAIL

    try:
        vacation = Vacation.objects.filter(pk=vacation_id)\
            .select_related('user').first()
    except Vacation.DoesNotExist:
        log.error('Vacation with `%s` id was not found.' % vacation_id)
        return None

    vacation.user.email_user(
        subject=_('Vacations'),
        message=_('You vacation was successfully created.'),
        from_email=FROM_EMAIL
    )

    recipient_list = []
    deliveries = Delivery.objects.filter(
        state=True,
        action_user=True
    )
    for delivery in deliveries:
        recipient_list.append(delivery.address)

    return send_mail(
        subject=_('Vacation created by %s') % vacation.user.get_full_name(),
        message=_('%s created new vacation %s - %s') % (
            vacation.user.get_full_name(),
            vacation.date_start.strftime('%Y-%m-%d'),
            vacation.date_end.strftime('%Y-%m-%d'),
        ),
        from_email=FROM_EMAIL,
        recipient_list=recipient_list
    )


@task(ignore_result=True, name='clear_old_rejected_vacations')
def clear_old_rejected_vacations():
    from vacation_app.models import Vacation
    from _vacation_project.settings import VACATION_REJECTED_DAYS_TO_REMOVE

    queryset = \
        Vacation.objects.filter(state=Vacation.VACATION_REJECTED_BY_ADMIN)
    if VACATION_REJECTED_DAYS_TO_REMOVE:
        date_to_remove = \
            datetime.now() - timedelta(days=VACATION_REJECTED_DAYS_TO_REMOVE)
        queryset = queryset.filter(updated_at__lte=date_to_remove)

    return queryset.delete()
