# Generated by Django 3.2.12 on 2022-03-28 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_auto_20220329_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='page_url',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.page', verbose_name='رابط الصفحة'),
        ),
    ]