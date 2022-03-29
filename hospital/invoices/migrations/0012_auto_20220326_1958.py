# Generated by Django 3.2.12 on 2022-03-26 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0011_auto_20220326_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='commercialRegister',
            field=models.IntegerField(unique=True, verbose_name='رقم السجل التجاري'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=200, verbose_name='اسم الشركة'),
        ),
        migrations.AlterField(
            model_name='department',
            name='head',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.person', verbose_name='رئيس القسم'),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=200, verbose_name='اسم القسم'),
        ),
        migrations.AlterField(
            model_name='item',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.department', verbose_name='القسم التابع له'),
        ),
        migrations.AlterField(
            model_name='item',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.invoice', verbose_name='مضاف للفاتورة'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=200, verbose_name='اسم العنصر'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(verbose_name='سعر الوحدة'),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.SmallIntegerField(verbose_name='الكمية المضافة'),
        ),
        migrations.AlterField(
            model_name='person',
            name='militaryNumber',
            field=models.IntegerField(unique=True, verbose_name='الرقم العسكري'),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=200, verbose_name='الاسم'),
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]