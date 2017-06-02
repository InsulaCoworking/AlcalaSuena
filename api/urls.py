from tastypie.api import Api

from api.resources import BandResource, VenueResource, EventResource, TagResource, SettingsResource, NewsResource


def get_api(version_name):

    api = Api(api_name=version_name)

    api.register(BandResource())
    api.register(VenueResource())
    api.register(EventResource())
    api.register(TagResource())
    api.register(SettingsResource())
    api.register(NewsResource())

    return api