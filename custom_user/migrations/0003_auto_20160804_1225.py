# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0002_auto_20160522_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 4, 12, 24, 59, 970862), verbose_name='date joined'),
        ),
    ]
