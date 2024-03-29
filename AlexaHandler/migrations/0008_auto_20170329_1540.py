# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 15:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AlexaHandler', '0007_clientsession_varnames'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NodeID', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='NodeFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FlowID', models.CharField(max_length=1000)),
                ('Nodes', models.ManyToManyField(to='AlexaHandler.Node')),
                ('Sess', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AlexaHandler.ClientSession')),
            ],
        ),
        migrations.AddField(
            model_name='node',
            name='NodeFlow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AlexaHandler.NodeFlow'),
        ),
        migrations.AddField(
            model_name='node',
            name='Sess',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AlexaHandler.ClientSession'),
        ),
        migrations.AddField(
            model_name='clientsession',
            name='NodeFlows',
            field=models.ManyToManyField(to='AlexaHandler.NodeFlow'),
        ),
    ]
