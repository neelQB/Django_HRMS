# Generated by Django 5.1.6 on 2025-02-17 09:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0010_alter_attendance_punch_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='punch_in',
            field=models.TimeField(default=datetime.time(2, 25, 30)),
        ),
    ]
