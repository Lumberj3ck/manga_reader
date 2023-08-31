from django.test import TestCase, RequestFactory
from reader.models import *
from django.conf import settings
from django.urls import reverse, resolve
import os, shutil
from .views import ChapterDetail, chapter_list, MangaListView


class Settings(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.m1 = Manga.objects.create(name="Dr-Stone", slug="dr-stone")
        cls.ch1 = Chapter.objects.create(
            name="King-of-jungles", manga=cls.m1, chapter_number=1
        )
        for i in range(2, 10):
            Chapter.objects.create(name=f"ch_name_{i}", manga=cls.m1, chapter_number=i)
        cls.p1 = Picture(chapter=cls.ch1)
        cls.folder_path = os.path.join(settings.MEDIA_ROOT, cls.ch1.name)


class ModelTest(Settings):
    def setUp(self):
        self.expected = os.path.join(self.ch1.name, "example.jpg")

    def tearDown(self):
        if os.path.exists(self.folder_path):
            shutil.rmtree(self.folder_path, ignore_errors=True)

    def test_upload(self):
        path = upload_to(self.p1, "example.jpg")
        self.assertEqual(path, self.expected)

    def test_new_picture(self):
        self.p1.img.save("example1.jpg", open("example.jpg", "rb"))
        os.path.exists(self.expected)

    def test_verbose_name(self):
        m_verb_name = self.m1._meta.get_field("name").verbose_name
        ch_verb_name = self.ch1._meta.get_field("name").verbose_name
        p1_verb_name = self.p1._meta.get_field("chapter").verbose_name
        self.assertEqual(m_verb_name, "Название манги")
        self.assertEqual(ch_verb_name, "Название главы")
        self.assertEqual(p1_verb_name, "Глава")

    def test_str(self):
        self.assertEqual(self.m1.__str__(), self.m1.name)
        self.assertEqual(self.ch1.__str__(), self.ch1.name)
        self.assertEqual(self.p1.__str__(), self.p1.img.name)

    ## URL TESTS


class UrlsTest(Settings):
    def test_manga_list_url(self):
        url = reverse("manga_list")
        self.assertEqual(url, "/")

    def test_chapter_list_url(self):
        url = reverse("chapter_list", kwargs={"manga_slug": self.m1.slug})
        self.assertEqual(url, f"/{self.m1.slug}/")

    def test_chapter_detail_url(self):
        url = reverse(
            "chapter_detail",
            kwargs={"manga_slug": self.m1.slug, "chapter_slug": self.ch1.name},
        )
        self.assertEqual(url, f"/{self.m1.slug}/{self.ch1.name}/")

    ## VIEW TESTS


class ViewTest(Settings):
    def test_manga_list_view(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["view"], MangaListView)
        self.assertQuerySetEqual(response.context["mangas"], Manga.objects.all())
        self.assertTemplateUsed(response, "reader/manga_list.html")

    def test_chapter_list_view(self):
        response = self.client.get(f"/{self.m1.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, chapter_list)
        self.assertTemplateUsed(response, "reader/chapter_list.html")

    def test_chapter_detail_view(self):
        response = self.client.get(f"/{self.m1.slug}/{self.ch1.name}/")
        self.assertEqual(response.status_code, 200)
        # self.assertIsInstance(response.resolver_match.func, ChapterDetail)
        self.assertTemplateUsed(response, "reader/chapter_detail.html")

    def test_chapter_detail_next_n_previous(self):
        self.ch2 = Chapter.objects.get(name="ch_name_2")
        response = self.client.get(f"/{self.m1.slug}/{self.ch1.name}/")
        self.assertEqual(response.context["next"], self.ch2)
        self.assertEqual(response.context["previous"], None)

    def test_chapter_detail_next(self):
        self.ch2 = Chapter.objects.get(name="ch_name_2")
        self.ch3 = Chapter.objects.get(name="ch_name_3")
        response = self.client.get(f"/{self.m1.slug}/{self.ch2.name}/")
        self.assertEqual(response.context["previous"], self.ch1)
        self.assertEqual(response.context["next"], self.ch3)

    def test_chapter_detail_last_next(self):
        self.last_chapter = Chapter.objects.get(name="ch_name_9")
        self.pre_last_chapter = Chapter.objects.get(name="ch_name_8")
        response = self.client.get(f"/{self.m1.slug}/{self.last_chapter.name}/")
        self.assertEqual(response.context["next"], None)
        self.assertEqual(response.context["previous"], self.pre_last_chapter)
