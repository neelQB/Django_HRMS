# Generated by Django 5.1.6 on 2025-02-12 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='employee_id',
            new_name='id',
        ),
    ]
