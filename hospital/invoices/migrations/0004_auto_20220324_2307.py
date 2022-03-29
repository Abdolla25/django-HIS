# Generated by Django 3.2.12 on 2022-03-24 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0003_auto_20220324_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='isDirectorAuth',
            field=models.CharField(choices=[('H', 'HOLD'), ('A', 'ACCEPTED'), ('R', 'REJECTED')], default='H', max_length=1, verbose_name='تصديق المدير؟'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='isFinanceAuth',
            field=models.CharField(choices=[('H', 'HOLD'), ('A', 'ACCEPTED'), ('R', 'REJECTED')], default='H', max_length=1, verbose_name='تصديق الماليات؟'),
        ),
    ]
