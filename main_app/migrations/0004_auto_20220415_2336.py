# Generated by Django 2.2.12 on 2022-04-15 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_grub_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='grub',
            name='desc',
            field=models.TextField(default='N/A', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grub',
            name='exp',
            field=models.DateField(verbose_name='exp date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grub',
            name='type',
            field=models.CharField(default='item', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grub',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grub',
            name='item',
            field=models.CharField(choices=[('F', 'Fresh Produce'), ('P', 'pantry')], default='P', max_length=1),
            preserve_default=False,
        ),
    ]