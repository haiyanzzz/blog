# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-24 07:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20171124_1334'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='article_poll',
            unique_together=set([('user', 'article')]),
        ),
    ]
