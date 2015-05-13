# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('uid', models.CharField(max_length=64, help_text='Will be auto-generated', primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1)),
                ('status', models.CharField(choices=[('new', 'New'), ('started', 'Started'), ('failed', 'Failed'), ('completed', 'Completed')], max_length=16)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('uid', models.CharField(max_length=64, help_text='Will be auto-generated', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('price_net', models.IntegerField()),
                ('price_total', models.IntegerField()),
                ('vat_rate', models.FloatField(default=0.23)),
                ('pkwiu_code', models.CharField(blank=True, max_length=16, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PayuPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(to='djangopay.Payment', primary_key=True, serialize=False, parent_link=True, auto_created=True)),
                ('payu_id', models.CharField(blank=True, max_length=128, null=True)),
            ],
            bases=('djangopay.payment',),
        ),
        migrations.AddField(
            model_name='payment',
            name='product',
            field=models.ForeignKey(to='djangopay.Product'),
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
