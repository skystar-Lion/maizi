# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-20 03:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='desc',
            field=models.CharField(max_length=250, unique=True, verbose_name='文章描述'),
        ),
    ]
