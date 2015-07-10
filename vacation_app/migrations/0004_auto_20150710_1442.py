# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacation_app', '0003_auto_20150703_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='rang',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='date_end',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='date_start',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='state',
            field=models.SmallIntegerField(default=1, db_index=True, choices=[(1, b'New'), (20, b'Approved by manager'), (21, b'Rejected by manager'), (30, b'Approved by admin'), (31, b'Rejected by admin')]),
        ),
    ]
