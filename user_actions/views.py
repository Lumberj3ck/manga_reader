from django.shortcuts import render
from django.contrib.postgres.search import TrigramSimilarity
from .forms import SearchForm
from reader.models import Chapter

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