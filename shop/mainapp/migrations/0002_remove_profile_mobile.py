# Generated by Django 3.1.7 on 2021-05-10 03:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='mobile',
        ),
    ]