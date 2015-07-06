# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacation_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='name',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AlterField(
            model_name='employee',
            name='group_code',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, b'User'), (2, b'Manager'), (3, b'Admin')]),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='state',
            field=models.SmallIntegerField(default=1, choices=[(1, b'New'), (20, b'Approved by manager'), (21, b'Rejected by manager'), (30, b'Approved by admin'), (31, b'Rejected by admin')]),
        ),
    ]
