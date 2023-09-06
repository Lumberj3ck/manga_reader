from django.shortcuts import render
from django.contrib import messages
from django.contrib.postgres.search import TrigramSimilarity
from .forms import SearchForm
from django.contrib.auth.decorators import login_required
from reader.models import Chapter, Manga
from django.views.decorators.http import require_POST
from account.models import Bookmark
from django.http import Http404, JsonResponse

@require_POST
def search(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        query = form.cleaned_data.get("query")
        chapters = (
            Chapter.objects.annotate(similarity=TrigramSimilarity("name", query))
            .filter(similarity__gt=0.3)
            .order_by("-similarity").select_related('manga')[:5]
        )
        second_search_results = Chapter.objects.filter(name__icontains=query).select_related('manga')[:5]
        empty = not chapters 
        return render(
            request,
            "user_actions/search_results.html",
            {
                "chapters": chapters,
                "second_chapters": second_search_results,
                "empty": empty,
                "query": query,
            },
        )
    return render(request, "user_actions/search_results.html", {"empty": True})

@require_POST
def bookmark(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'invalid_login'})
    chapter_slug = request.POST['chapter_slug']
    manga_slug = request.POST['manga_slug']
    try:
        manga = Manga.objects.get(slug=manga_slug)
        chapter = Chapter.objects.get(name=chapter_slug)
    except:
        return JsonResponse({'status': 'error'})
    if manga_slug and chapter_slug:
        previous_bookmark = Bookmark.objects.filter(manga=manga, profile=request.user.profile)
        if previous_bookmark:
            previous_bookmark[0].chapter = chapter
            previous_bookmark[0].save()
        else:
            Bookmark.objects.create(manga=manga, profile=request, chapter=chapter)
        return JsonResponse({'status': 'ok'})
    else:
        raise Http404(_('Manga and chapter required parameters'))
