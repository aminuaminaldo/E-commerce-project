# Generated by Django 4.0.2 on 2022-03-13 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscriber',
            old_name='date_addedd',
            new_name='date_added',
        ),
    ]
