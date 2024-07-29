from django import template
from django.urls import reverse


register = template.Library()


@register.filter
def get_url(item):
    if item.url:
        return item.url
    if item.named_url:
        return reverse(item.named_url)
    return '#'
