# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('vacation_app', '0012_auto_20160524_1300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacation',
            options={'verbose_name': 'Vacation', 'verbose_name_plural': 'Vacations'},
        ),
        migrations.AddField(
            model_name='vacation',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 29, 10, 50, 28, 638285, tzinfo=utc), verbose_name='Created at', auto_created=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vacation',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 29, 10, 50, 31, 18526, tzinfo=utc), verbose_name='Updated at', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='action_admin',
            field=models.BooleanField(default=True, verbose_name='Action admin'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='action_manager',
            field=models.BooleanField(default=True, verbose_name='Action manager'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='action_user',
            field=models.BooleanField(default=True, verbose_name='Action user'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='address',
            field=models.EmailField(unique=True, max_length=20, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='state',
            field=models.BooleanField(default=True, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='group_code',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Group code', choices=[(1, b'User'), (2, b'Manager'), (3, b'Admin')]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='rang',
            field=models.CharField(max_length=20, null=True, verbose_name='Rang', blank=True),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='comment_admin',
            field=models.TextField(null=True, verbose_name='Admin comment', blank=True),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='comment_user',
            field=models.TextField(null=True, verbose_name='User comment', blank=True),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='date_end',
            field=models.DateField(verbose_name='Date end', db_index=True),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='date_start',
            field=models.DateField(verbose_name='Date start', db_index=True),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='state',
            field=models.SmallIntegerField(default=1, db_index=True, verbose_name='State', choices=[(1, b'New'), (20, b'Approved by manager'), (21, b'Rejected by manager'), (30, b'Approved by admin'), (31, b'Rejected by admin')]),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
    ]
