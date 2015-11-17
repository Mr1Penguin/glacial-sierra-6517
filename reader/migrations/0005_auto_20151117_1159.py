# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0004_user_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=255)),
                ('last_use', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='token',
        ),
        migrations.AddField(
            model_name='site',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user_token',
            name='user_id',
            field=models.ForeignKey(to='reader.User'),
        ),
    ]
