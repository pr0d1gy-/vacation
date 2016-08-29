from django.core.mail import send_mail
from django.utils.timezone import datetime, timedelta

from celery.task import task


@task(ignore_result=True, name='delivery_send')
def delivery_send(subject, message, group_code):
    from vacation_app.models import Delivery, Employee

    delivery = Delivery.objects.all()
    recipient_list = []
    for item in delivery:
        if not item.state:
            continue

        if group_code == Employee.GUSER:
            if item.action_user:
                recipient_list.append(item.address)

        elif group_code == Employee.GMGER:
            if item.action_manager:
                recipient_list.append(item.address)

        elif group_code == Employee.GADMIN:
            if item.action_admin:
                recipient_list.append(item.address)

    send_mail(
        subject=subject,
        message=message,
        from_email='vacation@sub1.lt01test.tk',
        recipient_list=recipient_list
    )


@task(ignore_result=True, name='mail_vacation_change')
def mail_vacation_change():
    pass


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
