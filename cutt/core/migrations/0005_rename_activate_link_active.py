# Generated by Django 4.0.5 on 2022-06-19 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_status_link_activate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='activate',
            new_name='active',
        ),
    ]
