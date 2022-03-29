# Generated by Django 3.2.12 on 2022-03-17 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_carousel_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carousel',
            name='img_src',
            field=models.CharField(default='home/img/carousel/', max_length=80),
        ),
        migrations.AlterField(
            model_name='carousel',
            name='priority',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Slide Order'),
        ),
    ]
