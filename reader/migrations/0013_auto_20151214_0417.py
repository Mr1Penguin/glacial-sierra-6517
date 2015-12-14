# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0012_site_isactive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='isActive',
        ),
        migrations.AddField(
            model_name='site',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
