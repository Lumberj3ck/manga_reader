from requests import request
import random, bs4, os, time
import slugify
import logging, django, re
from django.conf import settings
from typing import List
from requests import Response
from image_size_reducer import image_reducer
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manga_reader.settings")
django.setup()
# settings.configure()
from reader.models import *


logging.basicConfig(
    level=logging.INFO,
    filename="parser.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/95.0.1020.30 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
]

headers = {
    "User-Agent": random.choice(user_agents),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Connection": "Connection",
    "cookie": "_gid=GA1.2.1125372524.1692948422; zone-cap-5050238=1%3B1692948427; _ga_1EBSXM5LQM=GS1.1.1692948422.3.1.1692948428.0.0.0; _ga=GA1.1.1727617779.1692773463",
}
main_folder = "./imgs"
manga_name = 'Attack on titan'
img_selector = '.text-center img'
def get_page(url:str):
    response = request(url=url, headers=headers, method="GET")
    return response


def get_img_in_ch(url:str):
    resp = get_page(url)
    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    imgs = soup.select(img_selector)
    links = [img.get("src") for img in imgs]
    return links


def write_into_file_and_save(response: Response, path_to_save, path_for_django, chapter_instance):
    if not os.path.exists(path_to_save):
        with open(path_to_save, "wb") as file:
            file.write(response.content)
            print(".", end="", flush=True)
        pic = Picture.objects.get_or_create(chapter=chapter_instance, img=path_for_django)
        image_reducer(picture_inst=pic[0])
    logging.info('already downloaded')


def make_folder_if_not_exists(folder):
    folder_path = os.path.join(main_folder, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        os.system(f'chown -R www-data:www-data {folder_path}')
    return folder_path

def download_chapter_imgs(urls, output_folder, chapter_instance):
    folder_path = make_folder_if_not_exists(output_folder)
    logging.info(f"Started downloading {folder_path}")
    for ind, link in enumerate(urls, start=1):
        response = get_page(link)
        picture_name = f"{ind}_img.jpg"
        path_for_django = os.path.join(output_folder, picture_name)
        path = os.path.join(folder_path, picture_name)
        if response.status_code == 200:
            write_into_file_and_save(response, path, path_for_django, chapter_instance)
        else:
            logging.warning(f"failed to download")


def get_chapter_links(url:str, selector:str, amount:int = "all") -> List[str]:
    response = get_page(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    raw_ch_links = soup.select(selector)
    if amount == "all":
        till = len(raw_ch_links)
    else:
        till = amount
    links = [link.get("href") for link in raw_ch_links[:till]]
    return links[::-1]


def create_chapter(chapter_name):
    match = re.search(pattern=r'\d+', string=chapter_name)
    if match:
        chapter_number = int(match.group())
    manga_inst = Manga.objects.filter(name=manga_name)[0]
    return Chapter.objects.get_or_create(name=chapter_name, manga=manga_inst, chapter_number=chapter_number)

def create_loop(chapter_links, site_url_split):
    for link in chapter_links:
        links = get_img_in_ch(link)
        folder_name = link.split(site_url_split)[1]
        print(folder_name)
        chapter_instance = create_chapter(folder_name)[0]
        download_chapter_imgs(links, folder_name, chapter_instance)
    logging.info("Success")

def main_parser(url:str, selector:str, site_url_split:str, amount:int='all') -> None:
    chapter_links = get_chapter_links(url=url, selector=selector, amount=amount)
    print(chapter_links)
    create_loop(chapter_links, site_url_split)

if __name__ == "__main__":
    ## do not forget about amount and -10 in get_Chapter_link
    # url1 = "https://stone-dr.com/"
    # selector1 = ".ceo_latest_comics_widget ul li a"
    # site_url_split = "https://stone-dr.com/manga/dr-stone-"
    selector = '.bg-bg-secondary .grid .col-span-3 a'
    url = "https://ww8.readsnk.com/manga/shingeki-no-kyojin/"
    site_url_split = "https://ww8.readsnk.com/chapter/"

    main_parser(url=url, selector=selector, site_url_split=site_url_split)






