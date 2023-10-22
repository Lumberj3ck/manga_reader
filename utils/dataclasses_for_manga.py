import re, json
from typing import List
from dataclasses import dataclass, field, asdict


class ChapterNotContainsDigit(Exception):
    pass


@dataclass
class Picture:
    picture_number: int
    picture_url: str
    medium_picture_url: str


@dataclass
class Chapter:
    name: str
    chapter_number: int = field(init=False)
    images: List[Picture]

    def __post_init__(self) -> None:
        match = re.search(r"\d+", self.name)
        if match:
            self.chapter_number = int(match[0])
        else:
            raise ChapterNotContainsDigit

@dataclass
class Manga:
    chapters: List[Chapter]
    manga_name: str = field(repr=False, default="aoashi")

@dataclass
class MangasList:
    mangas: List[Manga]

# loop trhough chapter on some site get pictures from one chapter 
# create picture name picture number
# at the end create chapter instance add name and images
# at a very end set Manga add every chapter make dict out of it and save to json
# at server read this json and create instances 


if __name__ == '__main__':
    img = Picture(picture_number=1, picture_url='asdfll', medium_picture_url='asdf')
    img1 = Picture(picture_number=2, picture_url='asdfll', medium_picture_url='asdf')
    s = Chapter(name="Chapter_1", images=[img, img1])
    manga = Manga(chapters=[s], manga_name='aoashi')
    manga1 = Manga(chapters=[s], manga_name='aoashi')

    json_dict = asdict(MangasList(mangas=[manga, manga1]))
    with open('test.json', 'w') as file:
        json.dump(json_dict, file)