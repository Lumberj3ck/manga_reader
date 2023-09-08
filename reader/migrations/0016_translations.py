# Generated by Django 4.2.3 on 2023-09-08 09:25

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0015_alter_chapter_chapter_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manga',
            name='name',
        ),
        migrations.CreateModel(
            name='MangaTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=200, verbose_name='Название манги')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='reader.manga')),
            ],
            options={
                'verbose_name': 'manga Translation',
                'db_table': 'reader_manga_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
    ]