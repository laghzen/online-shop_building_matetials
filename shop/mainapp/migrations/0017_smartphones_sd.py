# Generated by Django 3.2.7 on 2021-09-20 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0016_remove_smartphones_sd'),
    ]

    operations = [
        migrations.AddField(
            model_name='smartphones',
            name='sd',
            field=models.BooleanField(default=True, verbose_name='Наличие SD'),
        ),
    ]