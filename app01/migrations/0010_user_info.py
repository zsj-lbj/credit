# Generated by Django 2.1.1 on 2021-04-23 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0009_auto_20210411_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255)),
                ('clickname', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('institute', models.CharField(max_length=255)),
                ('img_src', models.CharField(max_length=255)),
            ],
        ),
    ]
