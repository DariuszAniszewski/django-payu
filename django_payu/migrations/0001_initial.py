# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PayuPayment',
            fields=[
                ('payment_id', models.CharField(serialize=False, max_length=64, primary_key=True, help_text='Will be auto-generated')),
                ('payment_status', models.CharField(max_length=16, choices=[('new', 'New'), ('started', 'Started'), ('failed', 'Failed'), ('completed', 'Completed')])),
                ('payu_id', models.CharField(blank=True, max_length=128, null=True)),
                ('buyer_first_name', models.CharField(max_length=64)),
                ('buyer_last_name', models.CharField(max_length=64)),
                ('buyer_email', models.EmailField(max_length=254)),
                ('buyer_ip_address', models.GenericIPAddressField()),
                ('product_name', models.CharField(max_length=128)),
                ('product_unit_price', models.IntegerField()),
                ('product_quantity', models.IntegerField(default=1)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True)),
                ('payu_messages_log', models.TextField()),
            ],
        ),
    ]
