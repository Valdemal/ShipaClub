# Generated by Django 2.2.5 on 2020-05-04 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainpage', '0003_auto_20200414_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Mainpage\\media', verbose_name='Изображение'),
        ),
    ]