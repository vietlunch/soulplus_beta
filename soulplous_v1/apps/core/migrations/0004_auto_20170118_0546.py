# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-01-18 05:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170118_0545'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='fullname',
            new_name='userfullname',
        ),
    ]
