# Generated by Django 2.2.12 on 2022-04-22 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_auto_20220422_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grub',
            name='exp',
            field=models.DateField(blank=True, null=True, verbose_name='exp date'),
        ),
    ]
