# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-28 22:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_auto_20171126_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='site_article_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.SiteArticleCategory', verbose_name='所属文章分类'),
        ),
    ]
