# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_payu', '0002_auto_20150531_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='payupayment',
            name='continue_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
