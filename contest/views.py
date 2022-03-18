# coding=utf-8
import csv
import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DeleteView

from bands import helpers
from bands.helpers import get_query
from bands.models import Tag, Band
from contest.forms.band import BandForm
from contest.forms.bandmember import BandMemberForm
from contest.forms.contest_criteria import ContestCriteriaForm
from contest.models import ContestBand, ContestJuryVote, ContestPublicVote


def bases(request):
    return render(request, 'contest/bases.html', {})

def contest_index(request):
    return render(request, 'contest/index.html', {})

def privacy_policy(request):
    return render(request, 'contest/privacy_policy.html', {})

def form_success(request):
    return render(request, 'contest/form_success.html', {})


class PrivacyPolicies(TemplateView):
    template_name = 'contest/privacy.html'

def signup(request):

    if settings.CONTEST_CLOSED:
        return render(request, 'contest/form_closed.html', {})

    members_factory = BandMemberForm.getMembersFormset()

    if request.method == "POST":
        form = BandForm(request.POST, request.FILES, initial={'is_new': True})
        members_formset = members_factory(request.POST, request.FILES, )

        if form.is_valid() and members_formset.is_valid():
            band = form.save(commit=False)

            band.save()
            form.save_m2m()
            BandMemberForm.save_members(band, members_formset)

            helpers.send_template_email(
                title='AlcalaSuena - Inscripción completa',
                destination= band.contact_email,
                template_name='signup_success',
                template_params={
                    'name':band.name,
                    'id':band.pk,
                }
            )

            return redirect('form_success')
        else:
            pass
            #print form.errors.as_data()
            #print members_formset.errors
    else:
        form = BandForm(initial={'is_new': True})
        members_formset = members_factory()

    categories = Tag.objects.current()

    return render(request, 'contest/form.html', {
        'categories': categories,
        'form': form,
        'members_formset': members_formset
    })

@login_required
def contest_dashboard(request):
    if not request.user.has_perm('contest.can_mange_jury'):
        if 'band' in request.session:
            band_pk = request.session['band']
            del request.session['band']
            band = ContestBand.objects.filter(pk=band_pk).first()

            num_votes = ContestPublicVote.objects.filter(voted_by=request.user).count()
            if num_votes >= 10:
                return redirect('contest_user_votes')

            vote, created = ContestPublicVote.objects.get_or_create(band=band, voted_by=request.user)
            vote.timestamp = datetime.datetime.now()
            vote.save()

            return redirect('contest_band_detail', pk=band.pk)

        return redirect('contest_user_votes')
    else:
        return redirect('contest_jury_list')

def contest_entries_list(request):
    bands = ContestBand.objects.current()
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
        params['tags'] = Tag.objects.current()
        return render(request, 'contest/list.html', params)


def contest_band_detail(request, pk):
    band = get_object_or_404(ContestBand, pk=pk)

    view_data = {
        'band': band,
        'num_votes': ContestPublicVote.objects.filter(band=band).count(),
        'jury_votes': ContestJuryVote.objects.filter(band=band),
        'view': request.GET.get('view', None)
    }

    if settings.PUBLIC_VOTE:
        voted = False
        if request.user.is_authenticated():
            voted = ContestPublicVote.objects.filter(band=band, voted_by=request.user).count() > 0
            view_data['voted'] = voted

    if request.user.has_perm('contest.can_mange_jury'):

        if request.method == "POST":
            form = ContestCriteriaForm(request.POST, instance=band)
            if form.is_valid():
                band = form.save(commit=False)
                if band.is_validated:
                    band.validated_by = request.user

                band.save()
        else:
            form = ContestCriteriaForm(instance=band)
        view_data['criteria_form'] = form

    if request.user.is_staff:
        band.jury_vote = ContestJuryVote.objects.filter(band=band, voted_by=request.user).first()

    return render(request, 'contest/band_detail.html', view_data )


class DeleteContestBand(UserPassesTestMixin, DeleteView):
    model = ContestBand
    success_url = reverse_lazy('contest_entries_list')
    template_name = 'contest/band_delete.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(DeleteContestBand, self).get_context_data(**kwargs)
        context['public_votes'] = ContestPublicVote.objects.filter(band=self.object).count()
        context['similar'] = ContestBand.objects.filter(name__contains=self.object.name[:15]).exclude(pk=self.object.pk)
        return context

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        target_band = request.POST.get('target_band', None)
        if target_band:
            target = ContestBand.objects.get(pk=target_band)
            for vote in ContestPublicVote.objects.filter(band=self.object):
                if not ContestPublicVote.objects.filter(band=target, voted_by=vote.voted_by).exists():
                    vote.band = target
                    vote.save()
                else:
                    vote.delete()

        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

@login_required
def contest_jury_list(request):

    if not request.user.has_perm('contest.can_mange_jury'):
        return HttpResponse('Unauthorized', status=401)

    bands = ContestBand.objects.current()
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

    if 'tovote' in request.GET:
        votes = ContestJuryVote.objects.filter(voted_by=request.user).values_list('band',flat=True)
        bands = bands.exclude(pk__in=votes)

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
        band.public_votes_count = ContestPublicVote.objects.filter(band=band).count()
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
        params['tags'] = Tag.objects.current()
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


def contest_band_validate(request, pk):
    band = get_object_or_404(ContestBand, pk=pk)
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    if request.method == "POST":
        band.is_validated = True
        band.save()

        return HttpResponse('Yeah!', status=200)
            #print members_formset.errors
    else:
        return HttpResponse('Unauthorized', status=401)

def contest_user_votes(request,):

    if not request.user.is_authenticated():
        return redirect('contest_social_login')

    votes = ContestPublicVote.objects.filter(voted_by=request.user)
    return render(request, 'contest/user_votes.html', {'votes': votes})

@login_required
def contest_csv_votes(request):
    if not request.user.has_perm('contest.can_mange_jury'):
        return HttpResponse('Unauthorized', status=401)

    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="votos_alcalasuena_' + now.strftime('%Y%m%d') + '.csv"'
    response.write(u'\ufeff'.encode('utf-8'))
    writer = csv.writer(response, dialect='excel', delimiter=str(';'), quotechar=str('"'))

    bands = ContestBand.objects.current()
    first_row = ['Banda', 'Miembros', 'Procedencia', 'Alcalaina', 'Categoria', 'Estilo', 'Pts total', 'Pts Criterios', 'Pts Jurado']

    juries = User.objects.filter(is_staff=True)
    for jury in juries:
        first_row.append(jury.username)

    writer.writerow(first_row)

    for band in bands:
        city = band.city.encode('utf-8').strip() if band.city else ''
        results = [band.name.encode('utf-8').strip(), band.num_members, city, band.has_local_member]
        results.append(band.tag.name.encode('utf-8'))
        results.append(band.genre.encode('utf-8').strip() if band.genre else '')
        results.append(str(band.total_points))
        results.append(str(band.criteria_points))
        results.append(str(band.jury_points))

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
    response.write(u'\ufeff'.encode('utf-8'))
    writer = csv.writer(response, dialect='excel', delimiter=str(';'), quotechar=str('"'))

    bands = ContestBand.objects.current()
    first_row = ['Banda', 'Email', 'Miembros', 'Alcalaina',]

    writer.writerow(first_row)

    for band in bands:
        results = [band.name.encode('utf-8').strip(), band.contact_email.encode('utf-8').strip(), band.num_members, band.has_local_member]
        writer.writerow(results)

    return response



@login_required
def contest_csv_user_votes(request):
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="votes_alcalasuena_' + now.strftime('%Y%m%d') + '.csv"'
    writer = csv.writer(response)

    users = User.objects.all()
    first_row = ['username', 'Usuario', 'Reqistro', 'Votos', ]

    writer.writerow(first_row)

    for user in users:
        num_votes = ContestPublicVote.objects.filter(voted_by=user).count()
        results = [user.username, user.get_full_name().encode('utf-8').strip(), str(user.date_joined), num_votes]
        writer.writerow(results)

    return response


@login_required
def contest_receiver_info(request):
    if not request.user.has_perm('contest.can_mange_jury'):
        return HttpResponse('Unauthorized', status=401)

    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ganadores_alcalasuena_' + now.strftime('%Y%m%d') + '.csv"'
    writer = csv.writer(response)

    bands = ContestBand.objects.current()
    first_row = ['Banda', 'Procedencia', 'Miembros de alcala', 'Interesado', 'NIF', 'Email', 'Telefono1', 'Telefono2']
    writer.writerow(first_row)

    for band in bands:
        if Band.objects.filter(name__icontains=band.name).exists():
            results = [band.name.encode('utf-8').strip(),
                       band.city.encode('utf-8').strip() if band.city else '',
                       'Si' if band.has_local_member else 'No',
                       band.receiver_fullname.encode('utf-8').strip(),
                       band.receiver_cif.encode('utf-8').strip(),
                       band.contact_email.encode('utf-8').strip(),
                       band.contact_phone1.encode('utf-8').strip(),
                       band.contact_phone2.encode('utf-8').strip() if band.contact_phone2 else '']
            writer.writerow(results)

    return response


@login_required
def contest_rider_info(request):
    if not request.user.has_perm('contest.can_mange_jury'):
        return HttpResponse('Unauthorized', status=401)

    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="riders_alcalasuena' + now.strftime('%Y%m%d') + '.csv"'
    response.write(u'\ufeff'.encode('utf-8'))
    writer = csv.writer(response, dialect='excel', delimiter=str(';'), quotechar=str('"'))

    bands = ContestBand.objects.current()
    first_row = ['Banda', 'Num miembros', 'Rider', 'Email', 'Telefono1', 'Telefono2']
    writer.writerow(first_row)

    for band in bands:
        if Band.objects.filter(name__icontains=band.name).count() > 0:
            results = [
                band.name.encode('utf-8').strip(),
                band.num_members,
                '' if not band.rider_doc else (settings.BASESITE_URL + band.rider_doc.url),
                band.contact_email.encode('utf-8').strip(),
                band.contact_phone1.encode('utf-8').strip(),
                band.contact_phone2.encode('utf-8').strip() if band.contact_phone2 else '']
            writer.writerow(results)

    return response


@login_required
def contest_participants_info(request):
    if not request.user.has_perm('contest.can_mange_jury'):
        return HttpResponse('Unauthorized', status=401)

    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="participantes_alcalasuena_' + now.strftime('%Y%m%d') + '.csv"'
    response.write(u'\ufeff'.encode('utf-8'))
    writer = csv.writer(response, dialect='excel', delimiter=str(';'), quotechar=str('"'))

    bands = ContestBand.objects.current()
    first_row = ['Banda', 'Procedencia', 'Miembros de alcala', 'Interesado', 'NIF', 'Email', 'Telefono1', 'Telefono2']
    writer.writerow(first_row)

    for band in bands:
        results = [
            band.name.encode('utf-8').strip(),
            band.city.encode('utf-8').strip() if band.city else '',
            'Si' if band.has_local_member else 'No',
            band.receiver_fullname.encode('utf-8').strip() if band.receiver_fullname else '',
            band.receiver_cif.encode('utf-8').strip() if band.receiver_cif else '',
            band.contact_email.encode('utf-8').strip(),
            band.contact_phone1.encode('utf-8').strip(),
            band.contact_phone2.encode('utf-8').strip() if band.contact_phone2 else '']
        writer.writerow(results)

    return response

def social_login(request):
    if request.user.is_authenticated():
        return redirect('contest_user_votes')

    band = request.GET.get('band', None)
    if band:
        request.session['band'] = band
    else:
        if request.session.get('band', False):
           del request.session['band']

    return render(request, 'contest/social_login.html')


def contest_public_vote(request, pk):
    band = get_object_or_404(ContestBand, pk=pk)

    if request.user.is_authenticated():

        if request.method == "POST":

            action = request.POST.get('action', 'add')
            if action == 'add':

                num_votes = ContestPublicVote.objects.filter(voted_by=request.user).count()
                if num_votes >= 10:
                    return HttpResponse('Too many votes!', status=403)

                vote, created = ContestPublicVote.objects.get_or_create(band=band, voted_by=request.user)
                vote.timestamp = datetime.datetime.now()
                vote.save()

                band_votes = ContestPublicVote.objects.filter(band=band).count()
                return JsonResponse({'band_votes':band_votes}, status=200)

            elif action == 'delete':
                ContestPublicVote.objects.filter(band=band, voted_by=request.user).delete()
                return HttpResponse('Yeah!', status=200)


    return HttpResponse('Unauthorized', status=401)
