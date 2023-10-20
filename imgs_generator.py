import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manga_reader.settings")
django.setup()
from reader.models import *


for pic in Picture.objects.all():
    pic.img = pic.img.replace('https://mangachapters.s3.eu-north-1.amazonaws.com', 'https://d27xvdd6r1e956.cloudfront.net')
    pic.medium_img = pic.medium_img.replace('https://mangachapters.s3.eu-north-1.amazonaws.com', 'https://d27xvdd6r1e956.cloudfront.net')
    pic.save()
    print(pic.img,'saved')
#manga = Manga.objects.get(slug='dr_stone')
#for chapter in range(30):
    # os.mkdir(f'imgs/chapter_{chapter}')
   # chapter_inst = Chapter.objects.create(manga=manga, chapter_number=chapter, name=f'chapter_{chapter}')
  #  for img in range(20):
        #       with open(f'imgs/chapter_{chapter}/img_{img}.jpg', 'w') as file:
 #           file.write('asdfasd')
#        with open(f'imgs/chapter_{chapter}/img_{img}_medium.jpg', 'w') as file:
            #           file.write('asdfasd')
#        Picture.objects.create(chapter=chapter_inst, img='some url', medium_img='medium img url')
