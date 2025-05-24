from django import template
from django.core.cache import cache

register = template.Library()

POPULAR_TAGS_CACHE_KEY = 'popular_tags_sidebar'

@register.inclusion_tag('layouts/popular_tags_sidebar.html')
def popular_tags_sidebar():
    popular_tags = cache.get(POPULAR_TAGS_CACHE_KEY)

    if popular_tags is None:
        popular_tags = []

    return {'popular_tags_list': popular_tags}

BEST_USERS_CACHE_KEY = 'best_users_sidebar'

@register.inclusion_tag('layouts/best_users_sidebar.html')
def best_users_sidebar():
    best_users = cache.get(BEST_USERS_CACHE_KEY)
    
    if best_users is None:
        best_users = []

    return {'best_users_list': best_users}