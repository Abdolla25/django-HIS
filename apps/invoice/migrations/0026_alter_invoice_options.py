# Generated by Django 3.2.13 on 2022-07-31 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0025_alter_invoice_entryperson'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'permissions': [('change_task_status', 'Can change the status of tasks'), ('close_task', 'Can remove a task by setting its status as closed')], 'verbose_name': 'فاتورة', 'verbose_name_plural': 'فواتير'},
        ),
    ]
