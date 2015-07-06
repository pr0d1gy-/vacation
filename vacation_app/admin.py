from django.contrib import admin

from vacation_app.models import Vacation, Delivery, Employee

admin.site.register(Vacation)
admin.site.register(Employee)
admin.site.register(Delivery)

