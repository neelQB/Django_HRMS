# Generated by Django 5.1.6 on 2025-02-19 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0012_alter_attendance_punch_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='working_hours_frompunch',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
