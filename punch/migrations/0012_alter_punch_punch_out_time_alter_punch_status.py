# Generated by Django 5.1.6 on 2025-02-25 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('punch', '0011_alter_punch_date_alter_punch_punch_in_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='punch',
            name='punch_out_time',
            field=models.DateTimeField(default=datetime.time(0, 0)),
        ),
        migrations.AlterField(
            model_name='punch',
            name='status',
            field=models.CharField(choices=[('PUNCHEDIN', 'PUNCHEDIN'), ('PUNCHEDOUT', 'PUNCHEDOUT')], default='PUNCHEDIN', max_length=20),
        ),
    ]
