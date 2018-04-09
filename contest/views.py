from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from bands.helpers import get_query
from bands.models import Tag
from contest.forms.band import BandForm
from contest.forms.bandmember import BandMemberForm
from contest.models import ContestBand


def bases(request):
    return render(request, 'contest/bases.html', {})

def form_success(request):
    return render(request, 'contest/form_success.html', {})

def signup(request):
    members_factory = BandMemberForm.getMembersFormset()

    if request.method == "POST":
        form = BandForm(request.POST, request.FILES, initial={'is_new': True})
        members_formset = members_factory(request.POST, request.FILES, )

        if form.is_valid() and members_formset.is_valid():
            band = form.save(commit=False)

            band.save()
            form.save_m2m()
            BandMemberForm.save_members(band, members_formset)

            return redirect('form_success')
        else:
            pass
            #print form.errors.as_data()
            #print members_formset.errors
    else:
        form = BandForm(initial={'is_new': True})
        members_formset = members_factory()

    categories = Tag.objects.all()

    return render(request, 'contest/form.html', {
        'categories': categories,
        'form': form,
        'members_formset': members_formset
    })


def contest_entries_list(request):
    bands = ContestBand.objects.all()
    band_count = bands.count()
    tag_filter = request.GET.get('tag', None)
    if tag_filter:
        bands = bands.filter(tag__pk=tag_filter)

    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['name', 'genre', 'city'])
        if entry_query:
            bands = bands.filter(entry_query)

    paginator = Paginator(bands, 9)
    page = request.GET.get('page')
    try:
        bands = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        bands = paginator.page(1)
    except (EmptyPage, InvalidPage):
        # If page is out of range (e.g. 9999), deliver last page of results.
        bands = paginator.page(paginator.num_pages)

    params = {
        'ajax_url': reverse('contest_entries_list'),
        'query_string': query_string,
        'band_count': band_count,
        'bands': bands,
        'page': page
    }

    if request.is_ajax():
        response = render(request, 'contest/search_results.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        params['tags'] = Tag.objects.all()
        return render(request, 'contest/list.html', params)


def contest_band_detail(request, pk):
    band = get_object_or_404(ContestBand, pk=pk)
    return render(request, 'contest/band_detail.html', {
        'band': band,
        'view': request.GET.get('view', None)
    })