from django.db.models.signals import post_save

from vacation_app.models.employee import Employee
from vacation_app.models.delivery import Delivery
from vacation_app.models.vacation import Vacation
from vacation_app.models.mails import send_mails


post_save.connect(send_mails, sender=Vacation)
