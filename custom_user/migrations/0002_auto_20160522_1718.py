# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 22, 17, 18, 15, 547529), verbose_name='date joined'),
        ),
    ]
