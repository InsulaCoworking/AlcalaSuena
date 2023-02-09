from django.conf import settings


def contest_status(request):
    return {
        'CONTEST_ACTIVE': settings.CONTEST_ACTIVE,
        'CONTEST_CLOSED': settings.CONTEST_CLOSED,
        'CONTEST_OPENING': settings.CONTEST_OPENING,
        'APP_VISIBLE': settings.APP_VISIBLE,
        'ARCHIVE_YEARS': settings.ARCHIVE_YEARS,
        'SCHEDULE_ACTIVE':settings.SCHEDULE_ACTIVE,
        'PUBLIC_VOTE': settings.PUBLIC_VOTE,
        'DELETE_ENABLED': settings.DELETE_ENABLED,
    }
