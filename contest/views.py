import csv
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from bands.helpers import get_query
from bands.models import Tag
from contest.forms.band import BandForm
from contest.forms.bandmember import BandMemberForm
from contest.models import ContestBand, ContestJuryVote


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

    return render(request, 'contest/form_closed.html', {
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
    if request.user.is_staff:
        band.jury_vote = ContestJuryVote.objects.filter(band=band, voted_by=request.user).first()

    jury_votes = ContestJuryVote.objects.filter(band=band)
    return render(request, 'contest/band_detail.html', {
        'band': band,
        'jury_votes': jury_votes,
        'view': request.GET.get('view', None)
    })

@login_required
def contest_jury_list(request):


    bands = ContestBand.objects.all()
    jury_count = User.objects.filter(is_staff=True).count()

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


    for band in bands:
        if request.user.is_staff:
            band.jury_vote = ContestJuryVote.objects.filter(band=band, voted_by=request.user).first()
        else:
            band.num_votes = ContestJuryVote.objects.filter(band=band).count()


    params = {
        'ajax_url': reverse('contest_jury_list'),
        'query_string': query_string,
        'jury_count': jury_count,
        'band_count': band_count,
        'bands': bands,
        'page': page
    }

    if request.is_ajax():
        response = render(request, 'contest/jury_results.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        params['tags'] = Tag.objects.all()
        return render(request, 'contest/jury_list.html', params)



def contest_band_vote(request, pk):
    band = get_object_or_404(ContestBand, pk=pk)
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    if request.method == "POST":
        jury_vote, created = ContestJuryVote.objects.get_or_create(band=band, voted_by=request.user)
        jury_vote.timestamp = datetime.datetime.now()

        vote = request.POST.get('vote', 1)
        jury_vote.vote = vote
        jury_vote.save()

        return HttpResponse('Yeah!', status=200)
            #print members_formset.errors
    else:
        return HttpResponse('Unauthorized', status=401)


@login_required
def contest_csv_votes(request):
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="votos_alcalasuena_' + now.strftime('%Y%m%d') + '.csv"'
    writer = csv.writer(response)

    bands = ContestBand.objects.all()
    first_row = ['Banda', 'Miembros', 'Procedencia', 'Alcalaina']

    juries = User.objects.filter(is_staff=True)
    for jury in juries:
        first_row.append(jury.get_full_name() if jury.first_name else jury.username)

    writer.writerow(first_row)

    for band in bands:
        results = [band.name.encode('utf-8').strip(), band.num_members, band.city.encode('utf-8').strip(), band.has_local_member]
        for jury in juries:
            jury_vote = ContestJuryVote.objects.filter(band=band, voted_by=jury).first()

            results.append('' if not jury_vote else str(jury_vote.vote))

        writer.writerow(results)

    return response



@login_required
def contest_csv_bands(request):
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bands_alcalasuena_' + now.strftime('%Y%m%d') + '.csv"'
    writer = csv.writer(response)

    bands = ContestBand.objects.all()
    first_row = ['Banda', 'Email', 'Miembros', 'Alcalaina',]

    writer.writerow(first_row)

    for band in bands:
        results = [band.name.encode('utf-8').strip(), band.contact_email, band.num_members, band.has_local_member]
        writer.writerow(results)

    return response