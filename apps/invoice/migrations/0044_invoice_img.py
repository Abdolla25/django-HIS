# Generated by Django 3.2.13 on 2022-08-21 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0043_alter_item_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='inv_images'),
        ),
    ]
