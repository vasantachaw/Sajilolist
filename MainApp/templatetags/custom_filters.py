from django import template
from django.utils.timesince import timesince
from django.contrib.contenttypes.models import ContentType
from MainApp.models import Wishlist

register = template.Library()

@register.filter
def underscore_to_space(value):
    if not value:
        return ''
    words = value.replace('_', ' ').lower().split()
    capitalized_words = [word.capitalize() for word in words[:2]] + words[2:]
    return ' '.join(capitalized_words)

@register.filter
def time_since_simple(value):
    if not value:
        return ""
    return timesince(value).split(',')[0] + " ago"

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def is_in(value, arg):
    return value in arg

@register.filter
def model_name(instance):
    return instance.__class__.__name__.lower()

@register.filter
def in_wishlist(user, product):
    if not user.is_authenticated:
        return False
    content_type = ContentType.objects.get_for_model(product)
    return Wishlist.objects.filter(user=user, content_type=content_type, object_id=product.pk).exists()


@register.filter
def map_country_code(value):
    return {
        '+977': '🇳🇵',
        '+1': '🇺🇸',
    }.get(value, value)
