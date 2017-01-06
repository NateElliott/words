# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-02 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_paper_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='file',
            field=models.FileField(default='old', upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paper',
            name='origin',
            field=models.TextField(default='old', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paper',
            name='status',
            field=models.TextField(default='public', max_length=128),
        ),
    ]