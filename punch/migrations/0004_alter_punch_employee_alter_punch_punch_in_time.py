# Generated by Django 5.1.6 on 2025-02-18 18:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('punch', '0003_alter_punch_punch_in_time_alter_punch_punch_out_time'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='punch',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='punch',
            name='punch_in_time',
            field=models.DateTimeField(),
        ),
    ]
