# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacation_app', '0011_auto_20150729_1559'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vacation',
            unique_together=set([('date_start', 'date_end', 'user', 'state')]),
        ),
    ]
