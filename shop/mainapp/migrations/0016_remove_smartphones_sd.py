# Generated by Django 3.2.7 on 2021-09-20 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_smartphones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smartphones',
            name='sd',
        ),
    ]
