# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-01-18 06:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20170118_0549'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='noteby',
            new_name='actionid',
        ),
        migrations.RenameField(
            model_name='note',
            old_name='notein',
            new_name='userid',
        ),
    ]
