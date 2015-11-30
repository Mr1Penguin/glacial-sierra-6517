# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0010_auto_20151130_1320'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='image',
            unique_together=set([]),
        ),
    ]
