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
    print recipient_list
    send_mail(subject, message, 'test@test.ua', recipient_list)
    print 'MAIL SENDED'
