# Generated by Django 3.2.12 on 2022-03-24 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20220324_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='details',
            field=models.CharField(default=5, max_length=200),
            preserve_default=False,
        ),
    ]
