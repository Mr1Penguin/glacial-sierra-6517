# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='add_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 11, 19, 36, 275300, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
