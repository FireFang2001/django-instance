# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-08 02:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uauth', '0005_userticket'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='userticket',
            table='bees_ticket',
        ),
    ]
