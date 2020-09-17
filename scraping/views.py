from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm


def list_view(request):
    city = request.GET.get("city")
    language = request.GET.get("language")
    form = FindForm()
    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
        qs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 10)  # Show 10 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)

def home_view(request):
    form = FindForm()
    return render(request, 'scraping/home.html', {'form': form})
