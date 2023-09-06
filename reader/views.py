from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import *
from django.http import Http404, HttpResponseRedirect, JsonResponse
from .models import *
from django.views import View
from django.shortcuts import get_object_or_404
from account.models import Bookmark
from .forms import CommentForm
from django.db.models import Count
from django.contrib.humanize.templatetags import humanize
import redis

r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)

def contact(request):
    return render(request, 'reader/contact.html')

@login_required
def bookmarks(request):
    bookmarks = request.user.profile.bookmarks.all() 
    return render(request, 'reader/bookmarks.html', {'bookmarks': bookmarks})

def landing_view(request):
    # return render(request, 'reader/landing.html')
    return render(request, 'reader/new_landing.html')

def most_viewed_chapters(request, manga_slug):
    """Gets chapter_ranking from redis and renders it in -views"""
    most_viewed_chapters = r.zrange("chapter_ranking", 0, -1, desc=True)[:10]
    most_viewed_chapters = [
        chapter_b.decode("utf8") for chapter_b in most_viewed_chapters
    ]
    chapters = list(Chapter.objects.filter(name__in=most_viewed_chapters))
    chapters.sort(key=lambda x: most_viewed_chapters.index(x.name))
    most_liked_chapters = Chapter.objects.annotate(total_likes=Count("likes")).order_by(
        "total_likes"
    )
    return render(
        request,
        "reader/most_viewed_chapters.html",
        {"most_viewed_chapters": chapters, "most_liked_chapters": most_liked_chapters},
    )


@require_POST
def chapter_action(request):
    chapter_query = Chapter.objects.filter(name=request.POST["slug"])
    if chapter_query:
        chapter_object = chapter_query[0]
        action = request.POST["action"]
        if request.user.is_authenticated:
            if action == "like":
                chapter_object.likes.add(request.user)
            elif action == "unlike":
                chapter_object.likes.remove(request.user)
            elif action == "comment":
                new_comment = Comment.objects.create(
                    user=request.user,
                    chapter=chapter_object,
                    text=request.POST["comment_text"],
                )
                return JsonResponse(
                    {
                        "status": "ok",
                        "user": new_comment.user.username,
                        "user_photo": new_comment.user.profile.photo.url,
                        "comment_text": new_comment.text,
                        "created_at": humanize.naturaltime(new_comment.created_at),
                    }
                )
            return JsonResponse({"status": "ok"})
        return JsonResponse({"status": "invalid_login"})
    return JsonResponse({"status": "error"})


def chapter_list(request, manga_slug):
    chapters = Chapter.objects.filter(manga__slug=manga_slug)
    if not chapters:
        raise Http404()
    #chapters = get_object_or_404(Chapter, manga__slug=manga_slug)
    # queryset1 = Manga.objects.filter(name=manga_slug).chapters
    return render(request, "reader/chapter_list.html", {"chapters": chapters})


class ChapterDetail(View):
    model = Chapter
    template_name = "reader/chapter_detail.html"
    context_object_name = "chapter"
    form_class = CommentForm
    ## name is unique hence i thought is would be redudant to save both of them slug and name
    slug_field = "name"

    def make_bookmark(self, request):
        current_chapter = self.current_chapter
        manga = current_chapter.manga
        if request.user.is_authenticated:
            query = Bookmark.objects.get_or_create(profile=request.user.profile, chapter=self.current_chapter, manga=manga)
            if query:
                bookmark = query[0]
                bookmark.manga = manga
                bookmark.chapter = current_chapter
                bookmark.save()
            else:
                Bookmark.objects.create(
                    profile=request.user.profile, chapter=current_chapter, manga=manga
                )

    def get_context_data(self):
        self.context = {}
        self.context["next"] = self.next[0] if self.next else None
        self.context["previous"] = self.previous[0] if self.previous else None
        self.context[self.context_object_name] = self.current_chapter
        self.context['images'] = Picture.objects.filter(chapter=self.current_chapter).order_by('id')
        self.context["form"] = self.form_class()
        self.context["comments"] = self.current_chapter.comment_set.order_by('-created_at').all()
        self.context["total_views"] = self.total_views

    def get_next_previous_chapter(self) -> None:
        current_chapter_number = self.current_chapter.chapter_number
        self.next = Chapter.objects.filter(chapter_number=current_chapter_number + 1)
        self.previous = Chapter.objects.filter(
            chapter_number=current_chapter_number - 1
        )

    def update_views(self):
        self.total_views = r.incr(f"chapter:{self.current_chapter.name}:views")
        r.zincrby("chapter_ranking", 1, self.current_chapter.name)

    def get_chapter_object(self, chapter_slug):
        self.current_chapter = get_object_or_404(self.model, name=chapter_slug)

    def get(self, request, chapter_slug, manga_slug):
        self.get_chapter_object(chapter_slug)
        self.get_next_previous_chapter()
        self.update_views()
        self.get_context_data()
        self.make_bookmark(request)
        return render(request, self.template_name, self.context)


class MangaListView(ListView):
    queryset = Manga.objects.all()
    context_object_name = "mangas"
