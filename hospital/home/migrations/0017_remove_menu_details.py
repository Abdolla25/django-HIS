# Generated by Django 3.2.12 on 2022-03-24 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_menu_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='details',
        ),
    ]