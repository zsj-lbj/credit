# Generated by Django 2.1.1 on 2021-04-23 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0010_user_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_info',
            name='id',
        ),
        migrations.AlterField(
            model_name='user_info',
            name='user',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
