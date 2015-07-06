from datetime import datetime, timedelta

from django.core.mail import send_mail

from celery.task import task, periodic_task
from celery.schedules import crontab

import vacation_app.models

@task(ignore_result=True, name='delivery_send')
def delivery_send(subject, message, group_code):
    delivary = vacation_app.models.Delivery.objects.all()
    for item in delivary:
        print item
        print item.state
        if item.state:
            recipient_list = []
            if group_code == vacation_app.models.Employee.GUSER:
                if item['action_user']:
                    recipient_list.append(item['address'])
            elif group_code == vacation_app.models.Employee.GMGER:
                if item['action_manager']:
                    recipient_list.append(item['address'])
            elif group_code == vacation_app.models.Employee.GADMIN:
                if item['action_admin']:
                    recipient_list.append(item['address'])
    print recipient_list
    # send_mail(subject, body, sender, recipient_list)
    print 'MAIL SENDED'
