# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0005_auto_20151117_1159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_token',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AddField(
            model_name='image',
            name='width',
            field=models.IntegerField(default=600),
        ),
    ]
