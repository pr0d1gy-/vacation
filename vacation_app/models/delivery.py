from django.db import models


class Delivery(models.Model):
    address = models.EmailField(max_length=20)
    name = models.CharField(max_length=20)
    state = models.BooleanField(default=True)
    action_user = models.BooleanField(default=True)
    action_manager = models.BooleanField(default=True)
    action_admin = models.BooleanField(default=True)

    def __str__(self):
        return self.address
