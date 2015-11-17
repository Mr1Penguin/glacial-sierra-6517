# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0006_auto_20151117_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.URLField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='site',
            name='url',
            field=models.URLField(max_length=2000),
        ),
    ]
