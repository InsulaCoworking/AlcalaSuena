import itertools

import re
from django import template

register = template.Library()


youtube_regex = '^https?://(?:www\.)?youtu(?:\.be|be\.com)/(?:\S+/)?(?:[^\s/]*(?:\?|&)vi?=)?([^#?&]+)'
vimeo_regex = '^https?:\/\/(?:www\.)?vimeo\.com\/(?:videos|video|channels|)?\/?(\d*)'

@register.inclusion_tag('common/embed.html')
def create_embed(url_or_embed):
    """
    Returns the embed code directly or the url ready to be injected
    """

    if 'iframe' in url_or_embed:
        return {
            'embed':True,
            'code': url_or_embed
        }
    else:
        embeds = []
        for line in url_or_embed.splitlines():
            m = re.match(youtube_regex, line)
            if m:
                embeds.append({
                    'youtube': True,
                    'link': m.group(1)
                })

            m = re.match(vimeo_regex, line)
            if m:
                embeds.append({
                    'vimeo': True,
                    'link': m.group(1)
                })

        return { 'embed':False, 'embeds':embeds }



