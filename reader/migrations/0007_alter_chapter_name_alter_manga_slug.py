# Generated by Django 4.2.4 on 2023-08-26 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0006_manga_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название главы'),
        ),
        migrations.AlterField(
            model_name='manga',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
