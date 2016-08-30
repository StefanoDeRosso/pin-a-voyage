# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0028_auto_20160804_1723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='created_date',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='created_date',
            new_name='created',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 4, 17, 30, 45, 141809)),
        ),
    ]
