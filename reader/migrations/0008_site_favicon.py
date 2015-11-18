# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0007_auto_20151118_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='favicon',
            field=models.URLField(max_length=2000, null=True),
        ),
    ]
