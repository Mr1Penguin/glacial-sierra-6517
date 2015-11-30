# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0009_auto_20151118_2010'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='image',
            unique_together=set([('url', 'site')]),
        ),
    ]
