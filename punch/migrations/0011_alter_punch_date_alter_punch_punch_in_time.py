# Generated by Django 5.1.6 on 2025-02-25 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('punch', '0010_alter_punch_punch_in_time_alter_punch_punch_out_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='punch',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='punch',
            name='punch_in_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
