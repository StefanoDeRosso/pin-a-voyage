# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0005_auto_20160804_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 4, 18, 29, 4, 223345), verbose_name='date joined'),
        ),
    ]
