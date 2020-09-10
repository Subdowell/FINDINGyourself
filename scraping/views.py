from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm


def home_view(request):
    city = request.GET.get("city")
    language = request.GET.get("language")
    form = FindForm()
    qs = []
    if city or language:
        _filter = {}
        if city:
            _filter['city__name'] = city
        if language:
            _filter['language__name'] = language
        qs = Vacancy.objects.filter(**_filter)
    return render(request, 'scraping/home.html', {'object_list': qs, 'form': form})

