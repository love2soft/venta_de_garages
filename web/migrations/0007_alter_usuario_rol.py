# Generated by Django 4.2.1 on 2023-06-03 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_alter_garage_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.BooleanField(default=True),
        ),
    ]
