# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_payu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payupayment',
            name='payment_description',
            field=models.TextField(default='Your description'),
        ),
        migrations.AlterField(
            model_name='payupayment',
            name='buyer_ip_address',
            field=models.GenericIPAddressField(protocol='IPv4'),
        ),
    ]
