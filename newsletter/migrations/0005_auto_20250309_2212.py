# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2025-03-09 22:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0004_auto_20250309_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletteropen',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 3, 9, 22, 12, 13, 474554, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newsletteropen',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2025, 3, 9, 22, 12, 21, 831422, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
