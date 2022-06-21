# Generated by Django 3.2.13 on 2022-06-17 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0008_auto_20220617_0443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='purchases',
        ),
        migrations.AddField(
            model_name='purchase',
            name='invoice',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='invoice.invoice', verbose_name='صنف'),
            preserve_default=False,
        ),
    ]
