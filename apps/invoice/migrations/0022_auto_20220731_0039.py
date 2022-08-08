# Generated by Django 3.2.13 on 2022-07-30 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0021_alter_item_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='invoice.category', verbose_name='تصنيف الصنف'),
        ),
        migrations.AlterField(
            model_name='item',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice', verbose_name='الفاتورة'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=200, verbose_name='صنف'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(verbose_name='سعر الوحدة'),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.FloatField(verbose_name='الكمية'),
        ),
    ]
