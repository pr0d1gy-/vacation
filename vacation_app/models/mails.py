from vacation_app.models.employee import Employee
from vacation_app.models.vacation import Vacation

from vacation_app import tasks


def send_mails(instance, created, **kwargs):
    groups = {}

    for item in Employee.GROUPS:
        groups.update({item[0]: item[1]})

    if created:
        group_code = instance.user.group_code
        subject = 'vacation create by '
        message = '%s created new vacation %s - %s' % (
            instance.user.username,
            instance.date_start.strftime("%Y-%m-%d"),
            instance.date_end.strftime("%Y-%m-%d")
        )

    else:
        subject = 'vacation update by '

        if instance.state in [Vacation.VACATION_APPROVED_BY_MANAGER,
                              Vacation.VACATION_REJECTED_BY_MANAGER]:
            group_code = Employee.GMGER

        elif instance.state in [Vacation.VACATION_APPROVED_BY_ADMIN,
                                Vacation.VACATION_REJECTED_BY_ADMIN]:
            group_code = Employee.GADMIN

        message = '%s wants on vacation %s - %s' % (
            instance.user.username,
            instance.date_start.strftime("%Y-%m-%d"),
            instance.date_end.strftime("%Y-%m-%d")
        )
    subject += groups[group_code]
    tasks.delivery_send.delay(subject=subject, message=message, group_code=group_code)
    # tasks.delivery_send(subject=subject, message=message, group_code=group_code)


def send_mail_result(instance, **kwargs):
    if instance.state in [Vacation.VACATION_APPROVED_BY_ADMIN, Vacation.VACATION_REJECTED_BY_ADMIN]:
        subject = 'Vacation'
        message = 'Your have result for you vacation'
        recipient_list = [instance.user.email]
        tasks.delivery_send.delay(subject=subject, message=message, recipient_list=recipient_list)