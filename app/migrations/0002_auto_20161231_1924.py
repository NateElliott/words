# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-31 23:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='file',
        ),
        migrations.AddField(
            model_name='paper',
            name='store',
            field=models.TextField(default='old', max_length=255),
            preserve_default=False,
        ),
    ]
