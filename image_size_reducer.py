from PIL import Image
import os, logging, django

os.environ["DJANGO_SETTINGS_MODULE"] = "manga_reader.settings"
django.setup()
from reader.models import Picture

logging.basicConfig(
    level=logging.INFO,
    filename="reducer.log",
    encoding="utf8",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class DoNotExistException(Exception):
    def __init__(self, message="Path does not exists"):
        self.message = message
        super().__init__(self.message)


def image_reduce(img_path: str) -> str:
    updated_path = img_path.replace(".jpg", "_medium.jpg")
    if not os.path.exists(img_path) or not os.path.isfile(img_path):
        raise DoNotExistException
    with Image.open(img_path) as im:
        new_width = int(im.size[0] * 0.85)
        new_height = int(im.size[1] * 0.85)
        try:
            im.resize([new_width, new_height], Image.BILINEAR).save(
                updated_path, format="jpeg"
            )
        except OSError:
            logging.warning(f"This img has problem with rgb {img_path}")


def directories_walker():
    for picture in Picture.objects.all():
        try:
            image_reduce(picture.img.path)
        except DoNotExistException:
            logging.warning(f"{picture.img.path} failed to load")
            logging.info("This path does not exists or it is not file")
        else:
            logging.debug("Successfuly reduced image")
            media_img_path = picture.medium_img.url.replace("/", os.path.sep)[1:]
            medium_img_path = media_img_path.replace(".jpg", "_medium.jpg")
            picture.medium_img = medium_img_path
            picture.save()


if __name__ == "__main__":
    directories_walker()
