# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-22 09:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0002_remove_promocode_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Event', to='tokens.Events'),
        ),
    ]
