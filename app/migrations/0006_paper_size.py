# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-02 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_paper_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='size',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
