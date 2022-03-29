# Generated by Django 3.2.12 on 2022-03-26 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0006_auto_20220326_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectorAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isDirectorAuth', models.CharField(choices=[('H', 'معلق'), ('A', 'مقبول'), ('R', 'مرفوض')], default='H', max_length=1, verbose_name='تصديق المدير؟')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.invoice', verbose_name='مسلسل الفاتورة')),
            ],
            options={
                'verbose_name': 'تصديق المدير',
                'verbose_name_plural': 'تصديقات المدير',
            },
        ),
        migrations.CreateModel(
            name='FinanceAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isFinanceAuth', models.CharField(choices=[('H', 'معلق'), ('A', 'مقبول'), ('R', 'مرفوض')], default='H', max_length=1, verbose_name='تصديق الماليات؟')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.invoice', verbose_name='مسلسل الفاتورة')),
            ],
            options={
                'verbose_name': 'تصديق المدير',
                'verbose_name_plural': 'تصديقات المدير',
            },
        ),
        migrations.DeleteModel(
            name='Auth',
        ),
    ]
