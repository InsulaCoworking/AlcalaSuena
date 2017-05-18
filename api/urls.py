from tastypie.api import Api

from api.resources import BandResource


def get_api(version_name):

    api = Api(api_name=version_name)

    api.register(BandResource())

    return api