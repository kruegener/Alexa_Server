# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-10 10:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AlexaHandler', '0015_node_vars'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockChainModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'block_chain', max_length=1000)),
                ('pickle', models.FilePathField(path=b'cache/')),
            ],
        ),
        migrations.CreateModel(
            name='BlockModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'block', max_length=1000)),
                ('Sess', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AlexaHandler.ClientSession')),
            ],
        ),
        migrations.AddField(
            model_name='blockchainmodel',
            name='Chain',
            field=models.ManyToManyField(to='AlexaHandler.BlockModel'),
        ),
        migrations.AddField(
            model_name='blockchainmodel',
            name='Sess',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AlexaHandler.ClientSession'),
        ),
    ]
