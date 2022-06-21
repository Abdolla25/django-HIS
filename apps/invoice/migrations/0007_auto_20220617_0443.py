# Generated by Django 3.2.13 on 2022-06-17 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0006_auto_20220617_0402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='purchases',
        ),
        migrations.AddField(
            model_name='invoice',
            name='purchases',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='invoice.purchase', verbose_name='أصناف الفاتورة'),
            preserve_default=False,
        ),
    ]