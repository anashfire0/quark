# Generated by Django 2.0.5 on 2018-06-04 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0004_auto_20180527_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='reminded_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Reminded count'),
        ),
    ]
