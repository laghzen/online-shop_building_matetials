# Generated by Django 3.2.7 on 2021-09-18 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_alter_buildingblocks_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Brick',
            new_name='Bricks',
        ),
    ]