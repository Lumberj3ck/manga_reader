import os, django, re


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manga_reader.settings")
django.setup()

from reader.models import Picture

for pict in Picture.objects.all():
    print(pict.img)
    pict_number = re.search(r'(\d+)(?=_img)', pict.img)[0]
    pict.picture_number = pict_number
    pict.save()
