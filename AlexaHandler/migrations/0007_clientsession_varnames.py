# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AlexaHandler', '0006_clientsession_sessionfile_sessionvar_sessionvarfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientsession',
            name='varNames',
            field=models.ManyToManyField(to='AlexaHandler.SessionVar'),
        ),
    ]
