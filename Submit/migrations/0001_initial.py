# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-03-12 04:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NoEmbed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('i_name', models.CharField(max_length=16)),
                ('i_img', models.ImageField(upload_to='embeds/%Y/%m/%d')),
            ],
        ),
    ]
