import boto3, os, django, dotenv, io
dotenv.load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manga_reader.settings_prod")
django.setup()

from image_parser import get_page
from reader.models import Chapter, Picture, Manga
bucket_name = "mangachapters"

s3 = boto3.client(
    service_name="s3",
    region_name=os.environ.get("aws_region_name"),
    aws_access_key_id=os.environ.get("aws_access_key"),
    aws_secret_access_key=os.environ.get("aws_secret_key"),
)

# loop through files on local for os.walk(folder)
#  folder_name = if folder name startswith chapter- manga_name = 'somename'
#  folder_name = manga_name + '/' + folder + '/'
#  s3.put_object(Bucket='mangachapters', Key=(folder_name))
#  s3.upload_file(Filename=filename, Bucket=bucket_name, Key=folder_name + filename)

# s3.list_objects(Bucket=bucketname, Prefix=manga_name)
#  for chapt in list:
#  chapter.key
#  s3.list_objects(Bucket=bucketname, Prefix=manga_name/key)
#  for img in chapters:
#       img.key
#  create Url = https/bucket_name/manga/chapter_key/img
#  Manga.objects.create(name=manga, img=poster)
#  Chapter.objects.create()
# chapter_number = re.get_int(chapter_name)
# manga_inst = Manga.objects.filter(name=manga_name)[0]
# Chapter.objects.get_or_create(name=chapter_name, manga=manga_inst, chapter_number=chapter_number)
# s3.put_object(Bucket='mangachapters', Key=(folder_name))
# s3.upload_file(Filename="nonlocal_research.py", Bucket=bucket_name, Key=folder_name + 'nonlocal.py')
# https://mangachapters.s3.eu-north-1.amazonaws.com/dr_stone/chapter_1/img1.jpg
# manage.py dumpdata --exclude=Picture

def get_img_url(folder_name):
    url = f'https://{bucket_name}.s3.{os.environ.get("aws_region_name")}.amazonaws.com/{folder_name}'
    return url


def save_to_db(img_path, medium_img_path):
    names = img_path.split('/')
    manga_inst = Manga.objects.get(slug=names[-3]) 
    chapter_inst = Chapter.objects.get(name=names[-2], manga=manga_inst) 
    Picture.objects.get_or_create(chapter=chapter_inst, img=img_path, medium_img=medium_img_path)
    

def s3_upload_in_binary(s3, bucket_name, file, key):
    s3.upload_fileobj(Fileobj=io.BytesIO(file), Bucket=bucket_name, Key=key)

if __name__ == "__main__":
    response = get_page('https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgfKbqzmTkLE0DUoipLnj2K07jOSqnJ8mj3wAKcGD8iMK2vRLN5hCIkKXRz8Zuv-or-zpLL2hDFyEN8v56S-5lJzag9RrrDeDNTdWzMlGlYeERhmdN_btobAAhMkDLJreVPDQ5wXjKZ2oWceph6hjU0T_jhsfGi9-oxD_aj3OBwqXdBaxmJWY9umhrp/s1600/01.jpg')
    s3.upload_fileobj(Fileobj=io.BytesIO(response.content), Bucket=bucket_name, Key='random_manga/chapter_1/img_1.jpg')
    # ind = 0
    # for root, dirs, files in os.walk("imgs"):
    #     medium_imgs = {}
    #     ind += 1
    # #if '18.5' not in root:
    # #    continue
    # #else:
    # #    print(ind, root)
    # #    break
    # # if ind < 283:
    # #     continue
    #     for img in files:
    #         if "shingeki" in root:
    #             manga_name = 'attack_on_titan'
    #         elif "chapter" in root:
    #             manga_name = 'dr_stone'
    #         else:
    #             continue

    #         chapter_name = root.split(os.sep)[1]
    #         folder_name = f'{manga_name}/{chapter_name}/{img}'
    #         s3.upload_file(Filename=os.path.join(root, img), Bucket=bucket_name, Key=folder_name)

    #         if '_medium.jpg' in img:
    #             name_not_medium = folder_name.replace('_medium.jpg', '.jpg')
    #             url = get_img_url(name_not_medium)
    #             medium_imgs[url] = get_img_url(folder_name)
        
    #     else:
    #         print(f'Saving chapter {ind}' , root)
    #         for img_path, medium_img_path in medium_imgs.items():
    #             save_to_db(img_path, medium_img_path)


