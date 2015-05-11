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
                ('uid', models.CharField(max_length=64, primary_key=True, serialize=False, help_text='Will be auto-generated')),
                ('quantity', models.IntegerField(default=1)),
                ('status', models.CharField(max_length=16, choices=[('new', 'New'), ('started', 'Started'), ('failed', 'Failed'), ('completed', 'Completed')])),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('uid', models.CharField(max_length=64, primary_key=True, serialize=False, help_text='Will be auto-generated')),
                ('name', models.CharField(max_length=128)),
                ('price_net', models.FloatField()),
                ('price_total', models.FloatField()),
                ('vat_rate', models.FloatField(default=0.23)),
                ('pkwiu_code', models.CharField(blank=True, null=True, max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='PayuPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(serialize=False, primary_key=True, to='django_pay.Payment', parent_link=True, auto_created=True)),
                ('payu_id', models.CharField(blank=True, null=True, max_length=128)),
            ],
            bases=('django_pay.payment',),
        ),
        migrations.AddField(
            model_name='payment',
            name='product',
            field=models.ForeignKey(to='django_pay.Product'),
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
