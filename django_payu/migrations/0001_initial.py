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
                ('uid', models.CharField(max_length=64, primary_key=True, help_text='Will be auto-generated', serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField(default=1)),
                ('status', models.CharField(max_length=16, choices=[('new', 'New'), ('started', 'Started'), ('failed', 'Failed'), ('completed', 'Completed')])),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name='PayuPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='django_payu.Payment', primary_key=True, serialize=False)),
                ('payu_id', models.CharField(blank=True, null=True, max_length=128)),
            ],
            bases=('django_payu.payment',),
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
