# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0011_auto_20151130_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
    ]
