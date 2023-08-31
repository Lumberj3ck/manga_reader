from requests import request
import random, bs4, os, time
import slugify
import logging, django, re
from django.conf import settings
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


def get_page(url):
    response = request(url=url, headers=headers, method="GET")
    return response


def get_img_in_ch(url):
    resp = get_page(url)
    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    imgs = soup.select("p img")
    links = [img.get("src") for img in imgs]
    return links


def write_into_file_and_save(response, path_to_save, path_for_django, chapter_instance):
    if not os.path.exists(path_to_save):
        with open(path_to_save, "wb") as file:
            file.write(response.content)
            print(".", end="", flush=True)
    pic = Picture.objects.get_or_create(chapter=chapter_instance, img=path_for_django)
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


def get_chapter_links(amount="all"):
    url = "https://stone-dr.com/"
    response = get_page(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    raw_ch_links = soup.select(".ceo_latest_comics_widget ul li a")
    if amount == "all":
        till = len(raw_ch_links)
    else:
        till = amount
    links = [link.get("href") for link in raw_ch_links[:till]]
    return links[::-1]


def create_chapter(chapter_name):
    match = re.search(pattern=r'\d+', string=chapter_name)
    if match:
        chapter_number = match.group()
    manga_inst = Manga.objects.filter(name='Dr Stone')[0]
    return Chapter.objects.get_or_create(name=chapter_name, manga=manga_inst, chapter_number=chapter_number)


if __name__ == "__main__":
    ## do not forget about amount and -10 in get_Chapter_link
    for link in get_chapter_links(amount='all'):
        links = get_img_in_ch(link)
        folder_name = link.split("https://stone-dr.com/manga/dr-stone-")[1][:-1]
        print(folder_name)
        chapter_instance = create_chapter(folder_name)[0]
        download_chapter_imgs(links, folder_name, chapter_instance)
    logging.info("Success")
