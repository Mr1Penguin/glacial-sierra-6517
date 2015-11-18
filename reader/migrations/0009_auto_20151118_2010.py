# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0008_site_favicon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.TextField(),
        ),
    ]
