# Generated by Django 2.1.1 on 2021-04-23 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0011_auto_20210423_2248'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_info',
            old_name='clickname',
            new_name='nickname',
        ),
    ]