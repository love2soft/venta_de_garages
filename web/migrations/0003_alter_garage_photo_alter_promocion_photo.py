# Generated by Django 4.1.9 on 2023-05-16 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_producto_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garage',
            name='photo',
            field=models.ImageField(default='noimage.png', upload_to='web/Template/media/'),
        ),
        migrations.AlterField(
            model_name='promocion',
            name='photo',
            field=models.ImageField(default='noimage.png', upload_to='web/Template/media/'),
        ),
    ]
