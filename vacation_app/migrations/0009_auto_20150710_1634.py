# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('vacation_app', '0008_auto_20150710_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(unique=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='username',
            field=models.CharField(validators=[django.core.validators.RegexValidator(b'^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', b'invalid')], max_length=30, blank=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', null=True, verbose_name='username'),
        ),
    ]
