# Generated by Django 3.2 on 2023-11-05 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfiles', '0002_auto_20231105_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='user',
            field=models.CharField(default='default', max_length=255),
        ),
        migrations.AddField(
            model_name='folder',
            name='user',
            field=models.CharField(default='default', max_length=255),
        ),
    ]
