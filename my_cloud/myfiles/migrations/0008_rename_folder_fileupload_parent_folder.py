# Generated by Django 3.2 on 2023-10-23 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myfiles', '0007_remove_folder_child_folder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileupload',
            old_name='folder',
            new_name='parent_folder',
        ),
    ]
