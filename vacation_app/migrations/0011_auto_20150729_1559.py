# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacation_app', '0010_auto_20150721_1342'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vacation',
            unique_together=set([('user', 'date_start', 'date_end', 'state')]),
        ),
    ]
