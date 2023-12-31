# Generated by Django 4.2.4 on 2023-08-26 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reader', '0007_alter_chapter_name_alter_manga_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, upload_to='', verbose_name='users/%Y/%m/%d/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reader.chapter', verbose_name='Последняя глава')),
                ('manga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reader.manga', verbose_name='Манга')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='account.profile', verbose_name='Профиль')),
            ],
        ),
    ]
