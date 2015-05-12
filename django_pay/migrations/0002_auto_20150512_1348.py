# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_pay', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price_net',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_total',
            field=models.IntegerField(),
        ),
    ]
