from django.shortcuts import render, redirect

# Create your views here.
from bands.models import Tag
from contest.forms.band import BandForm
from contest.forms.bandmember import BandMemberForm


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