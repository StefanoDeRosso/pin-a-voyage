# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0003_auto_20160804_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 4, 17, 23, 30, 575282), verbose_name='date joined'),
        ),
    ]
