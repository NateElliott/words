# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-02 14:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170102_0955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='file',
        ),
    ]
