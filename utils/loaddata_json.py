import json, django, os, sys
from pathlib import Path

# Add the parent directory (manga_reader) to the sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manga_reader.settings_prod")
django.setup()
from reader.models import *

chapters = json.load(open('db_chapters.json', 'r'))

MANGA_SLUG = 'aoashi'
manga = Manga.objects.get(slug=MANGA_SLUG)
for ch in chapters['chapters']:
    manga_chapter = Chapter.objects.create(name=ch['name'], chapter_number=ch['chapter_number'], manga=manga)

    for picture in ch['images']:
        Picture.objects.create(picture_number=picture['picture_number'], chapter=manga_chapter, img=picture['picture_url'], medium_img=picture['medium_picture_url'])

