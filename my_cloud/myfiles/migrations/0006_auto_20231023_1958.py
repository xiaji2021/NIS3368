# Generated by Django 3.2 on 2023-10-23 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myfiles', '0005_auto_20231023_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='child_id',
        ),
        migrations.RemoveField(
            model_name='folder',
            name='parent_id',
        ),
    ]