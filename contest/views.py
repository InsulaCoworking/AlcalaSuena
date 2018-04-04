from django.shortcuts import render

# Create your views here.
def bases(request):
    return render(request, 'contest/bases.html', {})

def signup(request):
    return render(request, 'contest/form.html', {})