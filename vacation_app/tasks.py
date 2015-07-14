from django.core.mail import send_mail

from celery.task import task

import vacation_app.models

@task(ignore_result=True, name='delivery_send')
def delivery_send(subject, message, group_code):
    delivary = vacation_app.models.Delivery.objects.all()
    recipient_list = []
    for item in delivary:
        if item.state:
            if group_code == vacation_app.models.Employee.GUSER:
                if item.action_user:
                    recipient_list.append(item.address)
            elif group_code == vacation_app.models.Employee.GMGER:
                if item.action_manager:
                    recipient_list.append(item.address)
            elif group_code == vacation_app.models.Employee.GADMIN:
                if item.action_admin:
                    recipient_list.append(item.address)
    for i in recipient_list:
        send_mail(subject, message, 'arseniysychev@gmail.com', [i])

@task(ignore_result=True, name='decision_made')
def decision_is_made(subject, message, recipient_list):
    send_mail(subject, message, 'arseniysychev@gmail.com', recipient_list)