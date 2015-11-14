# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0002_image_add_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collect_date', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='image',
            name='add_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='site',
            name='add_date',
            field=models.DateTimeField(),
        ),
    ]
