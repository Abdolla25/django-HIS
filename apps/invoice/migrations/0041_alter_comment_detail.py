# Generated by Django 3.2.13 on 2022-08-08 22:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0040_alter_invoice_current_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='detail',
            field=models.CharField(default=django.utils.timezone.now, max_length=200, verbose_name='ملاحظة'),
            preserve_default=False,
        ),
    ]