# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-15 20:36
from __future__ import unicode_literals

import apps.producto.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0004_auto_20171213_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(upload_to=apps.producto.models.user_directory_path),
        ),
    ]
