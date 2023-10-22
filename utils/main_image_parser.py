from image_parser import *
from s3_bucket_uploader import s3, s3_upload_in_binary
from image_size_reducer import byte_image_reduce
from dataclasses_for_manga import Picture, Chapter, Manga, asdict
import logging, json


# get_chapter_links('url', 'selector')  returns links list
# get_img_in_ch(url, img_selector)
logging.basicConfig(
    level=logging.INFO,
    filename="main_parser.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def medium_img_process(img_byte, img_name):
    medium_img_bytes = byte_image_reduce(img_byte)
    medium_img_name = img_name.replace(".jpg", "_medium.jpg")
    print(f"{folder_name}/{medium_img_name}")
    # logging.info(f"{folder_name}/{medium_img_name}")
    path = folder_name + "/" + medium_img_name
    s3_upload_in_binary(
        s3=s3,
        bucket_name="mangachapters",
        file=medium_img_bytes,
        key=path,
    )
    return path


def parse_chapter(chapter_url) -> list:
    url_parts = chapter_url.split("/")
    return url_parts[-2]


def process_images(imgs_link: list, folder_name):
    for idx, img_link in enumerate(imgs_link[::]):
        response = get_page(img_link)
        img_name = f"{idx}_img.jpg"
        img_path = folder_name + "/" + img_name

        print(img_path)
        s3_upload_in_binary(
            s3=s3,
            bucket_name="mangachapters",
            file=response.content,
            key=img_path,
        )
        medium_img_path = medium_img_process(response.content, img_name)
        picture_inst = Picture(
            picture_number=idx, picture_url=site_url + img_path, medium_picture_url=site_url + medium_img_path
        )
        chapter_images.append(picture_inst)


manga_name = "ao_ashi"
chapter_selector = "#ceo_latest_comics_widget-3 ul li a"
img_selector = ".entry-content .separator a img"
site_url = 'https://d27xvdd6r1e956.cloudfront.net/'
chapter_links = get_chapter_links("https://w3.ao-ashi-manga.com/", chapter_selector)
chapters = []

for chapter_link in chapter_links[::]:
    logging.info(f"Started parsing")
    img_links = get_img_in_ch(chapter_link, img_selector)
    chapter_name = parse_chapter(chapter_link)
    folder_name = manga_name + "/" + chapter_name
    print(folder_name)
    chapter_images = []
    process_images(img_links, folder_name)
    chapter_inst = Chapter(name=chapter_name, images=chapter_images)
    chapters.append(chapter_inst)

manga = Manga(chapters=chapters, manga_name=manga_name)
json_dict = asdict(manga)
with open('db_chapters.json', 'w') as file:
    json.dump(json_dict, file)
