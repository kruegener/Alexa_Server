# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 15:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AlexaHandler', '0008_auto_20170329_1540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nodeflow',
            name='Nodes',
        ),
    ]
