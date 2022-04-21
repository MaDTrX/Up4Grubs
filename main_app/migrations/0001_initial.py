from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Grub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(default='Enter Item', max_length=50)),
                ('type', models.CharField(choices=[('Fresh Produce', 'Fresh'), ('Pantry', 'Pantry')], default='Fresh Produce', max_length=50)),
                ('exp', models.IntegerField(default=2022, verbose_name='exp date')),
                ('desc', models.TextField(default='Enter Description', max_length=250)),
                ('price', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('grub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.grub')),
            ],
        ),
    ]
