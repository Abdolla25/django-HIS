# Generated by Django 3.2.12 on 2022-03-29 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_alter_page_pure_html'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carousel',
            name='btn_url',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.page', verbose_name='رابط زر الضغط'),
        ),
    ]
