# coding=utf-8
import csv
import io
import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from bands import helpers
from bands.forms.billing_info import BillingForm
from bands.models import Band
from bands.models.billing_info import BillingInfo


@login_required
def billing_list(request):

    bills = BillingInfo.objects.all()
    bands_nobilling = Band.objects.filter(billinginfo__isnull=True)
    return render(request, 'billing/list.html', {'bills':bills, 'pending': bands_nobilling})

def billing_form(request):
    save_success = False
    if request.method == "POST":
        form = BillingForm(request.POST, request.FILES)
        #print form.is_valid()
        if form.is_valid():
            bill = form.save()
            #print bill
            save_success = True
            form = BillingForm()
    else:
        form = BillingForm()
    return render(request, 'billing/form.html', { 'form': form, 'save_success': save_success})

@login_required
def download_csv(request):
    bills = BillingInfo.objects.all()

    output = io.BytesIO()
    #BOM header to make it Excel-compliant
    output.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(output, delimiter=';', dialect='excel')
    writer.writerow(['Subido', 'Banda', 'CIF/NIF', 'Contacto', 'Email', 'Teléfono',
                     'Escenario', 'Num miembros', 'Total', 'Factura', 'Más de una banda', 'Comentarios'])

    for bill in bills:
        additional_text = bill.additional_text.encode('utf8') if bill.additional_text else None
        writer.writerow([bill.uploaded, bill.band.name.encode('utf8'), bill.cif, bill.contact_name.encode('utf8'), bill.contact_email.encode('utf8'), bill.contact_phone,
                         bill.venue.name.encode('utf8'), bill.num_members, bill.billing_total, request.scheme + '://' + request.META['HTTP_HOST']  + bill.billing_file.url, bill.multiple_bands, additional_text])

    response = HttpResponse(output.getvalue(), content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename="billing.csv"'

    return response


@login_required
def csv_bands(request):
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bands_alcalasuena_' + now.strftime('%Y%m%d') + '.csv"'
    writer = csv.writer(response)

    bands = Band.objects.all()
    first_row = ['Banda', 'Email', 'Enlaces']

    writer.writerow(first_row)

    for band in bands:
        media = helpers.get_media_urls(band.embed_media)
        media.extend(helpers.get_media_urls(band.embed_code))

        results = [band.name.encode('utf-8').strip(), '&&&'.join(media)]

        writer.writerow(results)

    return response
