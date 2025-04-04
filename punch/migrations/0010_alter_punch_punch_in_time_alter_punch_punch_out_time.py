# Generated by Django 5.1.6 on 2025-02-25 10:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('punch', '0009_alter_punch_punch_in_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='punch',
            name='punch_in_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='punch',
            name='punch_out_time',
            field=models.DateTimeField(blank=True, default=datetime.time(0, 0), null=True),
        ),
    ]
