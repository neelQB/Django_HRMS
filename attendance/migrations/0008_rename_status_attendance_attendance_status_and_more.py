# Generated by Django 5.1.6 on 2025-02-14 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0007_alter_attendance_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='status',
            new_name='attendance_status',
        ),
        migrations.AddField(
            model_name='attendance',
            name='punch_status',
            field=models.CharField(choices=[('PUNCHEDIN', 'PUNCHEDIN'), ('PUNCHEDOUT', 'PUNCHEDOUT')], default='PUNCHEDOUT', max_length=15),
        ),
    ]
