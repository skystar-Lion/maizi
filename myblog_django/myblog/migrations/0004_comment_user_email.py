# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-21 02:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0003_auto_20170420_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user_email',
            field=models.CharField(max_length=30, null=True, verbose_name='联系方式'),
        ),
    ]
