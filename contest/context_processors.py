from django.conf import settings


def contest_status(request):
    return {
        'CONTEST_ACTIVE': settings.CONTEST_ACTIVE,
        'CONTEST_CLOSED': settings.CONTEST_CLOSED,
    }
