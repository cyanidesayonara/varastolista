# Generated by Django 2.1.2 on 2018-11-26 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_auto_20181123_2244'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='part',
            options={'ordering': ('created_at',)},
        ),
    ]
