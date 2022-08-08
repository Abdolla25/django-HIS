# Generated by Django 3.2.13 on 2022-07-30 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0013_purchase_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='date_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='last_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='slug',
            field=models.SlugField(blank=True, max_length=500, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='company',
            name='uniqueId',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='commercialRegister',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='رقم السجل التجاري'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='اسم الشركة'),
        ),
    ]
